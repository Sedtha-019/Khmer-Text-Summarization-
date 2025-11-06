const inputDiv = document.getElementById("input");
const output1Div = document.getElementById("output1");
const output2Div = document.getElementById("output2");
const timer1 = document.getElementById("timer1");
const timer2 = document.getElementById("timer2");

let timerInterval1, timerInterval2;

// Auto-select API based on host
const API_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:5000/summarize"
  : "http://18.141.8.123:5000/summarize";

// Clear input and outputs
function clearInput() {
  inputDiv.innerHTML = "";
  output1Div.innerHTML = "";
  output2Div.innerHTML = "";
  resetTimer(timer1);
  resetTimer(timer2);
}

// Copy function
function copyOutput(outputId) {
  const outputDiv = document.getElementById(outputId);
  const text = outputDiv.textContent.trim();
  if (!text) return alert("មិនមានលទ្ធផលសម្រាប់ចម្លងទេ។");
  navigator.clipboard.writeText(text).then(() => alert("លទ្ធផលត្រូវបានចម្លង!"));
}

// Reset timer
function resetTimer(timerDiv) {
  clearInterval(timerDiv.timerInterval);
  timerDiv.innerText = "🕒 0.000s";
  timerDiv.style.color = "#555";
}

// Summarize text with real-time timers
async function summarizeText() {
  const text = inputDiv.textContent.trim();
  if (!text) return alert("សូមបញ្ចូលអត្ថបទសង្ខេប។");

  const model1 = document.getElementById("model-select-1").value;
  const model2 = document.getElementById("model-select-2").value;

  // Reset outputs
  output1Div.innerText = "កំពុងសង្ខេប...";
  output2Div.innerText = "កំពុងសង្ខេប...";
  resetTimer(timer1);
  resetTimer(timer2);

  // Start timers
  startTimer(timer1);
  startTimer(timer2);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text, models: [model1, model2] }),
    });

    const data = await response.json();

    // Stop timers
    stopTimer(timer1, true);
    stopTimer(timer2, true);

    // Fill outputs
    output1Div.innerText = data.results[model1]?.summary || "គ្មានលទ្ធផល";
    output2Div.innerText = data.results[model2]?.summary || "គ្មានលទ្ធផល";

  } catch (err) {
    console.error(err);
    stopTimer(timer1, false);
    stopTimer(timer2, false);
    output1Div.innerText = "កំហុសក្នុងការតភ្ជាប់";
    output2Div.innerText = "កំហុសក្នុងការតភ្ជាប់";
  }
}

// Timer helpers
function startTimer(timerDiv) {
  const start = performance.now();
  timerDiv.style.color = "#dc3545"; // red while running

  timerDiv.timerInterval = setInterval(() => {
    const elapsed = ((performance.now() - start) / 1000).toFixed(3);
    timerDiv.innerText = `🕒 ${elapsed}s`;
  }, 50);
}

function stopTimer(timerDiv, success) {
  clearInterval(timerDiv.timerInterval);
  timerDiv.style.color = success ? "#28a745" : "#dc3545"; // green if success, red if fail
}


// Clear outputs if input is empty
inputDiv.addEventListener("input", () => {
  if (!inputDiv.textContent.trim()) {
    output1Div.innerHTML = "";
    output2Div.innerHTML = "";
  }
});

// Language Switcher JavaScript
let currentLang = 'en';

function switchLanguage(lang) {
    if (currentLang === lang) return;
    
    currentLang = lang;
    
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    
    // Remove active class from all language elements
    document.querySelectorAll('[data-lang]').forEach(el => {
        el.classList.remove('active');
    });
    
    // Add active class to selected language elements
    document.querySelectorAll(`[data-lang="${lang}"]`).forEach(el => {
        el.classList.add('active');
    });
    
    // Update button states
    document.querySelectorAll('.lang-btn').forEach((btn) => {
        btn.classList.remove('active');
    });
    
    // Set active button
    event.currentTarget.classList.add('active');
    
    // Save preference to localStorage
    try {
        localStorage.setItem('preferredLanguage', lang);
    } catch (e) {
        console.log('Unable to save language preference');
    }
}

// Load saved language preference on page load
document.addEventListener('DOMContentLoaded', function() {
    try {
        const savedLang = localStorage.getItem('preferredLanguage');
        if (savedLang && (savedLang === 'km' || savedLang === 'en')) {
            currentLang = savedLang;
            
            // Update content
            document.querySelectorAll('[data-lang]').forEach(el => {
                el.classList.remove('active');
            });
            document.querySelectorAll(`[data-lang="${savedLang}"]`).forEach(el => {
                el.classList.add('active');
            });
            
            // Update buttons
            document.querySelectorAll('.lang-btn').forEach((btn, index) => {
                btn.classList.remove('active');
                if ((savedLang === 'en' && index === 0) || (savedLang === 'km' && index === 1)) {
                    btn.classList.add('active');
                }
            });
        }
    } catch (e) {
        console.log('Unable to load language preference');
    }
});
