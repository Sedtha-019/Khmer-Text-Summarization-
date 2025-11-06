// DOM Elements
const inputDiv = document.getElementById("input");
const outputDiv = document.getElementById("output");

// Clear input and outputs
function clearInput() {
    inputDiv.innerHTML = "";
    outputDiv.innerHTML = "";
}

// Copy input text
function copyInputText() {
    const text = inputDiv.textContent.trim();
    if (!text) return alert("មិនមានអត្ថបទសម្រាប់ចម្លងទេ។");
    navigator.clipboard.writeText(text).then(() => alert("អត្ថបទត្រូវបានចម្លង!"));
}

// Copy output text
function copyOutput() {
    const text = outputDiv.textContent.trim();
    if (!text) return alert("មិនមានលទ្ធផលសម្រាប់ចម្លងទេ។");
    navigator.clipboard.writeText(text).then(() => alert("លទ្ធផលត្រូវបានចម្លង!"));
}

// Check spelling - Main function
async function checkSpelling() {
    const text = inputDiv.textContent.trim();
    if (!text) return alert("សូមបញ្ចូលអត្ថបទដើម្បីពិនិត្យ។");

    // Show loading state
    const checkBtn = document.querySelector(".btn-spellcheck");
    const originalHTML = checkBtn.innerHTML;
    checkBtn.innerHTML = '<span class="checking-spinner"></span> កំពុងពិនិត្យ...';
    checkBtn.disabled = true;
    outputDiv.innerHTML = "កំពុងពិនិត្យអក្ខរាវិរុទ្ធ...";

    try {
        // Call spell check API
        const response = await fetch("/spellcheck", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text }),
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            outputDiv.innerHTML = "";
            return;
        }

        // Display corrected text
        outputDiv.textContent = data.corrected_text || "មិនអាចពិនិត្យបានទេ។";

    } catch (err) {
        console.error("Error:", err);
        alert("មានបញ្ហាក្នុងការពិនិត្យអក្ខរាវិរុទ្ធ។ សូមព្យាយាមម្ដងទៀត។");
        outputDiv.innerHTML = "";
    } finally {
        // Reset button
        checkBtn.innerHTML = originalHTML;
        checkBtn.disabled = false;
    }
}

// Clear output if input is empty
inputDiv.addEventListener("input", () => {
    if (!inputDiv.textContent.trim()) {
        outputDiv.innerHTML = "";
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
