const API_URL = "https://ai-powered-email-automated-spam-detector.onrender.com";

async function checkSpam() {
  const input = document.getElementById("emailInput");
  const btn = document.getElementById("checkBtn");
  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");
  const confidenceText = document.getElementById("confidenceText");

  const text = input.value.trim();

  if (!text) {
    alert("Please paste some email text first.");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Checking...";

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || "Server error");
    }

    const data = await response.json();

    resultBox.classList.remove("hidden", "spam", "not-spam");
    resultBox.classList.add(data.result === "spam" ? "spam" : "not-spam");
    resultText.textContent = data.result === "spam" ? "⚠️ Spam" : "✅ Not Spam";
    confidenceText.textContent = data.confidence
      ? `Confidence: ${data.confidence}%`
      : "";

  } catch (err) {
    resultBox.classList.remove("hidden", "spam", "not-spam");
    resultBox.classList.add("spam");
    resultText.textContent = "Error checking email";
    confidenceText.textContent = err.message || "Is the backend server running?";
  } finally {
    btn.disabled = false;
    btn.textContent = "Check Email";
  }
}