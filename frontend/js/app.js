// app.js — Day 2 version.
// DUMMY_RESULTS below stands in for what the real backend will return from
// POST /recommend on Day 3+. The shape matches what upload_schemes.py /
// the eligibility engine will actually produce, so swapping in the real
// fetch() call later shouldn't require changing renderResults() at all.

const DUMMY_RESULTS = [
  {
    schemeName: "NSFDC Micro Credit Finance Scheme",
    eligible: true,
    matchScore: 92,
    reasons: [
      "Category matches scheme target group (SC)",
      "Income is within the ₹3,00,000 limit",
      "Project cost is within the ₹1.40 lakh limit",
    ],
    emi: { monthlyEmi: 3805, totalInterest: 12250 },
    requiredDocuments: ["SC caste certificate", "Income certificate", "Identity proof"],
    officialSourceUrl: "https://nsfdc.nic.in/en/micro-credit-finance",
  },
  {
    schemeName: "NSFDC Term Loan Scheme",
    eligible: true,
    matchScore: 78,
    reasons: [
      "Category matches scheme target group (SC)",
      "Income is within the ₹3,00,000 limit",
      "Requested amount is well within the ₹45,00,000 limit",
    ],
    emi: { monthlyEmi: 4980, totalInterest: 46200 },
    requiredDocuments: ["SC caste certificate", "Income certificate", "Project report"],
    officialSourceUrl: "https://nsfdc.nic.in/en/term-loan",
  },
  {
    schemeName: "Stand-Up India Scheme",
    eligible: false,
    matchScore: 21,
    reasons: [
      "This scheme requires a greenfield (brand new) enterprise — an existing business does not qualify",
    ],
    emi: null,
    requiredDocuments: [],
    officialSourceUrl: "https://www.standupmitra.in/",
  },
];

function renderResults(results) {
  const container = document.getElementById("results-list");
  if (!container) return;

  if (!results || results.length === 0) {
    container.innerHTML = `<p class="text-muted">No matching schemes found. Try adjusting your details.</p>`;
    return;
  }

  container.innerHTML = results.map(renderSchemeCard).join("");
}

function renderSchemeCard(scheme) {
  const badge = scheme.eligible
    ? `<span class="badge badge-eligible">Potentially eligible</span>`
    : `<span class="badge badge-ineligible">Not eligible</span>`;

  const reasons = (scheme.reasons || []).map(r => `<li>${escapeHtml(r)}</li>`).join("");

  const emiBlock = scheme.emi
    ? `<p class="mb-1"><strong>Estimated EMI:</strong> ₹${scheme.emi.monthlyEmi.toLocaleString("en-IN")}/month</p>`
    : "";

  const docsBlock = (scheme.requiredDocuments && scheme.requiredDocuments.length)
    ? `<p class="mb-1 mt-2"><strong>Documents needed:</strong></p><ul>${scheme.requiredDocuments.map(d => `<li>${escapeHtml(d)}</li>`).join("")}</ul>`
    : "";

  return `
    <div class="col-md-6 col-lg-4">
      <div class="scheme-card">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <h5>${escapeHtml(scheme.schemeName)}</h5>
          <span class="match-score">${scheme.matchScore}</span>
        </div>
        ${badge}
        <ul class="mt-3">${reasons}</ul>
        ${emiBlock}
        ${docsBlock}
        <a href="${scheme.officialSourceUrl}" target="_blank" rel="noopener" class="d-block mt-3 small">Official source ↗</a>
      </div>
    </div>
  `;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// Profile form: for now (Day 2), just carries you to the results page.
// On Day 3, this becomes a real fetch() POST to /recommend.
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("profile-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    // Day 3 TODO: collect these values and POST them to /recommend instead
    // of just redirecting straight to the dummy results page.
    window.location.href = "results.html";
  });
});