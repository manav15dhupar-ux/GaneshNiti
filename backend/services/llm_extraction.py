# """
# llm_extraction.py — Day 3 second deliverable.

# WHAT THIS DOES:
# Takes a user's free-text description of their financing need and converts it
# into structured fields (category, income, amount, purpose, etc.) using an
# LLM API call.

# WHAT THIS DOES NOT DO (read this before touching this file):
# This file NEVER decides eligibility. It has no scheme data, no rule logic,
# no pass/fail decisions. Its only job is turning messy human language into
# clean structured data that eligibility_engine.py can then check. If you ever
# feel tempted to add "and if income is low, mark them eligible" logic here --
# don't. That belongs in eligibility_engine.py, where it can be tested and
# audited as a plain, deterministic rule.

# WHY THE VALIDATION STEP MATTERS:
# LLMs occasionally return malformed JSON, or invent a field that doesn't
# belong, or skip a field. This file NEVER trusts the LLM's raw output --
# every response is checked against ExtractedProfile below before anything
# downstream sees it. If validation fails, we fall back to whatever structured
# form fields the user already typed, rather than crashing or guessing.

# HOW TO SET THIS UP:
# 1. Get an API key from whichever LLM provider your team is using
#    (Anthropic, OpenAI, etc. -- this file uses Anthropic's API as the
#    example; swap the client call if your team uses a different provider).
# 2. Set it as an environment variable, never hardcoded:
#        export ANTHROPIC_API_KEY="your-key-here"
# 3. pip install anthropic pydantic

# HOW TO TEST WITHOUT SPENDING API CREDITS:
# Run this file directly -- it includes a --mock mode that skips the real API
# call and returns a fake response, so you can test the validation and
# fallback logic for free before wiring in a real key.
#     python llm_extraction.py --mock
# """

# import json
# import os
# import sys
# from typing import Optional

# from pydantic import BaseModel, ValidationError, field_validator


# class ExtractedProfile(BaseModel):
#     """The ONLY shape of data this module is allowed to hand back.
#     Anything the LLM returns that doesn't fit this shape gets rejected."""
#     category: Optional[str] = None
#     state: Optional[str] = None
#     annual_income: Optional[float] = None
#     business_type: Optional[str] = None
#     purpose: Optional[str] = None
#     amount_required: Optional[float] = None
#     is_new_business: Optional[bool] = None

#     @field_validator("annual_income", "amount_required")
#     @classmethod
#     def must_be_non_negative(cls, v):
#         if v is not None and v < 0:
#             raise ValueError("Amount cannot be negative")
#         return v


# EXTRACTION_PROMPT = """You are a data extraction tool. You do NOT decide eligibility \
# or give financial advice. Your only job is to read the person's description of their \
# financing need and pull out structured fields.

# Return ONLY a JSON object with these exact keys (use null for anything not mentioned):
# {{
#   "category": string or null (e.g. "SC", "ST", "OBC", "General"),
#   "state": string or null,
#   "annual_income": number or null (in rupees, no commas or symbols),
#   "business_type": string or null,
#   "purpose": string or null (what the money is for, e.g. "equipment purchase"),
#   "amount_required": number or null (in rupees, no commas or symbols),
#   "is_new_business": boolean or null (true if starting fresh, false if expanding an existing business)
# }}

# Do not include any text before or after the JSON. Do not invent values that \
# weren't stated or clearly implied.

# Person's description:
# \"\"\"{user_text}\"\"\"
# """


# def _mock_llm_call(user_text: str) -> str:
#     """Fake LLM response for testing without API credits or a key."""
#     return json.dumps({
#         "category": "SC",
#         "state": "Maharashtra",
#         "annual_income": 280000,
#         "business_type": "tailoring",
#         "purpose": "equipment purchase",
#         "amount_required": 120000,
#         "is_new_business": False,
#     })


# def _real_llm_call(user_text: str) -> str:
#     """Calls the actual LLM API. Swap this function's body if your team uses
#     a different provider -- the rest of the file doesn't need to change."""
#     try:
#         import anthropic
#     except ImportError:
#         raise RuntimeError("Run: pip install anthropic")

#     api_key = os.environ.get("ANTHROPIC_API_KEY")
#     if not api_key:
#         raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable first.")

#     client = anthropic.Anthropic(api_key=api_key)
#     response = client.messages.create(
#         model="claude-haiku-4-5-20251001",  # fast + cheap is fine for pure extraction
#         max_tokens=300,
#         messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(user_text=user_text)}],
#     )
#     return response.content[0].text


# def extract_structured_data(user_text: str, form_fields: Optional[dict] = None, use_mock: bool = False) -> dict:
#     """
#     Main entry point. Returns a dict matching ExtractedProfile's fields.

#     form_fields: whatever the user already typed into the structured form
#     (category, state, income, etc.) -- used as a SAFE FALLBACK if the LLM
#     call fails or returns something that doesn't validate. This means a
#     broken LLM call never crashes the app or blocks a recommendation.
#     """
#     form_fields = form_fields or {}

#     if not user_text or not user_text.strip():
#         # No free text given -- just use whatever the structured form provided.
#         return form_fields

#     try:
#         raw_response = _mock_llm_call(user_text) if use_mock else _real_llm_call(user_text)
#         parsed = json.loads(raw_response)
#         validated = ExtractedProfile(**parsed)
#         result = validated.model_dump(exclude_none=True)
#         # Structured form fields fill in anything the LLM didn't catch.
#         return {**form_fields, **result}

#     except (json.JSONDecodeError, ValidationError, RuntimeError) as e:
#         print(f"[llm_extraction] Extraction failed ({e}) -- falling back to structured form fields only.")
#         return form_fields


# if __name__ == "__main__":
#     use_mock = "--mock" in sys.argv
#     sample_text = "I run a small tailoring business and want to buy two more sewing machines. I need around 1.2 lakh rupees."

#     print(f"Testing extraction ({'MOCK' if use_mock else 'REAL API'} mode)...")
#     print(f"Input: {sample_text}\n")

#     result = extract_structured_data(sample_text, form_fields={"category": "SC", "state": "Maharashtra"}, use_mock=use_mock)
#     print("Extracted:")
#     print(json.dumps(result, indent=2))