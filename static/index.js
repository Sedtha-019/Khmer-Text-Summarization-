const inputDiv = document.getElementById("input");
const output1Div = document.getElementById("output1");
const output2Div = document.getElementById("output2");

// ✅ Auto API selection
const API_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:5000/summarize"
  : "https://khmer-text-summarization-y7gh.onrender.com/summarize";  // TODO: change to your URL

// Clear input and outputs
function clearInput() {
  inputDiv.innerHTML = "";
  output1Div.innerHTML = "";
  output2Div.innerHTML = "";
}

// Copy input text
function copyInputText() {
  const text = inputDiv.textContent.trim();
  if (!text) return alert("មិនមានអត្ថបទសម្រាប់ចម្លងទេ។");
  navigator.clipboard.writeText(text).then(() => alert("អត្ថបទត្រូវបានចម្លង!"));
}

// Copy output text
function copyOutput(outputId) {
  const outputDiv = document.getElementById(outputId);
  const text = outputDiv.textContent.trim();
  if (!text) return alert("មិនមានលទ្ធផលសម្រាប់ចម្លងទេ។");
  navigator.clipboard.writeText(text).then(() => alert("លទ្ធផលត្រូវបានចម្លង!"));
}

// ✅ Summarize function
async function summarizeText() {
  const text = inputDiv.textContent.trim();
  if (!text) return alert("សូមបញ្ចូលអត្ថបទសង្ខេប។");

  const model1 = document.getElementById("model-select-1").value;
  const model2 = document.getElementById("model-select-2").value;

  output1Div.innerHTML = "កំពុងសង្ខេប...";
  output2Div.innerHTML = "កំពុងសង្ខេប...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text, models: [model1, model2] }),
    });

    const data = await response.json();

    if (data.results) {
      output1Div.innerText = data.results[model1]?.summary || "គ្មានលទ្ធផល";
      output2Div.innerText = data.results[model2]?.summary || "គ្មានលទ្ធផល";
    } else {
      alert("មានបញ្ហាក្នុងការសង្ខេប។");
    }
  } catch (err) {
    console.error(err);
    output1Div.innerText = "កំហុសក្នុងការតភ្ជាប់";
    output2Div.innerText = "កំពុងព្យាយាមឡើងវិញ...";
    alert("មានបញ្ហាក្នុងការសង្ខេប។ សូមព្យាយាមម្ដងទៀត។");
  }
}

// Clear outputs if input is empty
inputDiv.addEventListener("input", () => {
  if (!inputDiv.textContent.trim()) {
    output1Div.innerHTML = "";
    output2Div.innerHTML = "";
  }
});
