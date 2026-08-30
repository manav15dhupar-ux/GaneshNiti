# SIH 2026 PS92 — AI-Driven NSFDC Scheme & Channel Partner Navigator

An AI-assisted web platform that helps Scheduled Caste entrepreneurs and students find the right NSFDC credit scheme (Micro Finance, Term Loan, or Educational Loan), understand if they're eligible, and find their nearest Channel Partner — without needing to understand government scheme jargon first.

**Core principle: AI understands the entrepreneur; verified rules evaluate eligibility.**
The AI never decides who is eligible. Deterministic, verifiable Python rules do that. The AI's only job is turning a person's plain-language description of their situation into structured data.

---

## How It Works

![Architecture Diagram](architecture_diagram.png)

1. A user fills in a short profile (category, state, income, business type) and describes their need in their own words.
2. The backend sends that free-text description to an LLM, which converts it into structured data — nothing more.
3. Verified scheme data (researched from official government sources) is checked against the user's structured profile using plain Python rules.
4. Eligible schemes are ranked by relevance, an EMI is calculated, and a nearby Channel Partner is suggested.
5. The frontend displays everything — including exactly *why* each scheme matched — back to the user.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML + Bootstrap + JavaScript |
| Backend | Python + FastAPI |
| Database | Firebase Firestore |
| AI | LLM API (natural-language understanding only) |
| Eligibility & Matching | Plain Python, deterministic rules — no ML |

Deliberately simple. No microservices, no vector databases, no custom-trained ML models — this is a 6-person student team building in 6 days plus a 24-hour hackathon.

---

## Project Structure

```
ps92-scheme-navigator/
  backend/          <- FastAPI app, eligibility engine, LLM calls
  frontend/         <- HTML/Bootstrap/JS pages
  data/             <- Scheme spreadsheet + Firestore upload script
  README.md         <- You are here
  architecture_diagram.png
```

---

## Running the Backend Locally

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser. You should see:
```json
{"message": "Hello World! The PS92 backend is alive."}
```

---

## Data

All scheme data lives in `data/PS92_Scheme_Research.xlsx`, researched and verified against official sources (nsfdc.nic.in, PIB press releases, and other government portals — every row lists its source and last-verified date).

To load this data into Firestore:
```
cd data
python upload_schemes.py --dry-run     # safe preview, no database needed
python upload_schemes.py               # real upload, needs a Firebase service account key
```

---

## Team

| Role | Member |
|---|---|
| Backend Lead | Dev A |
| Backend/Data | Dev B |
| Frontend Lead | Dev C |
| Frontend/UI | Dev D |
| Data/QA | Dev E |
| Documentation/Presentation | Doc |

---

## Status

- [x] Scheme research spreadsheet — verified against official sources
- [x] Firestore upload script — built and dry-run tested
- [ ] Firestore live upload
- [ ] Eligibility engine
- [ ] LLM extraction
- [ ] Matching/ranking + EMI calculator
- [ ] Frontend integration
- [ ] Testing & demo prep