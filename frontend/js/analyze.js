const form = document.getElementById("analyzeForm");
const resultDiv = document.getElementById("result");
const loadingDiv = document.getElementById("loading");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  // Basic frontend validation
  if (
    !formData.get("offer_text") &&
    !formData.get("website_url") &&
    !formData.get("linkedin_url") &&
    !formData.get("screenshot").name
  ) {
    alert("Please provide at least one input.");
    return;
  }

  loadingDiv.classList.remove("hidden");
  resultDiv.classList.add("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze/", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    document.getElementById("scoreValue").innerText =
      `Scam Score: ${data.scam_score}%`;

    const riskBadge = document.getElementById("riskLevel");
    riskBadge.innerText = data.risk_level;
    riskBadge.className = `badge ${data.risk_level}`;

    const flagsList = document.getElementById("redFlags");
    flagsList.innerHTML = "";
    data.red_flags.forEach(flag => {
      const li = document.createElement("li");
      li.innerText = flag;
      flagsList.appendChild(li);
    });

    document.getElementById("summary").innerText =
      data.analysis_summary;

    resultDiv.classList.remove("hidden");

  } catch (error) {
    alert("Error analyzing offer. Please try again.");
    console.error(error);
  } finally {
    loadingDiv.classList.add("hidden");
  }
});
