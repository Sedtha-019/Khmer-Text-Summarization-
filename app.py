from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import torch
from peft import PeftModel
import warnings
import re
from transformers import (
    MBartForConditionalGeneration, MBart50Tokenizer,
    MT5ForConditionalGeneration, T5Tokenizer,
    AutoModelForTokenClassification, AutoTokenizer
)

# ================== Config ==================
load_dotenv()
app = Flask(__name__)

warnings.filterwarnings("ignore", category=FutureWarning)

# ================== Device ==================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ================== Models Configuration ==================
MODELS = {
    "model1": {
        "name": "Model 1 - Khmer MBart Summarization",
        "repo": "sedtha/mBart-50-large_LoRa_kh_sumerize",
        "type": "mbart",
        "model": None,
        "tokenizer": None
    },
    "model2": {
        "name": "Model 2 - Khmer mT5 Summarization",
        "repo": "angkor96/khmer-mT5-news-summarization",
        "type": "mt5",
        "model": None,
        "tokenizer": None
    }
}

# Spell checking model configuration
SPELL_CHECK_MODEL = {
    "name": "Khmer Spell Checker",
    "model": None,
    "tokenizer": None
}

# ================== Load Models ==================
def load_model(model_key):
    """Lazy-load the specified model and tokenizer"""
    model_info = MODELS[model_key]

    if model_info["model"] is None:
        try:
            print(f"🔹 Loading {model_info['name']}...")

            if model_info["type"] == "mbart":
                tokenizer = MBart50Tokenizer.from_pretrained(
                    model_info["repo"],
                    src_lang="km_KH",
                    tgt_lang="km_KH",
                    cache_dir="./cache"
                )

                base_model = MBartForConditionalGeneration.from_pretrained(
                    "facebook/mbart-large-50",
                    cache_dir="./cache"
                ).to(device)

                model = PeftModel.from_pretrained(
                    base_model,
                    model_info["repo"],
                    cache_dir="./cache"
                ).to(device)

            elif model_info["type"] == "mt5":
                tokenizer = T5Tokenizer.from_pretrained(model_info["repo"], cache_dir="./cache")
                model = MT5ForConditionalGeneration.from_pretrained(model_info["repo"], cache_dir="./cache").to(device)

            else:
                raise ValueError("Unknown model type")

            model.eval()
            model_info["model"] = model
            model_info["tokenizer"] = tokenizer
            print(f"✅ {model_info['name']} loaded successfully on {device}.")

        except Exception as e:
            print(f"❌ Failed to load {model_info['name']}: {e}")
            raise

    return model_info["model"], model_info["tokenizer"]

def load_spell_check_model():
    """Load spell checking model"""
    if SPELL_CHECK_MODEL["model"] is None:
        try:
            print(f"🔹 Loading Khmer Spell Checker...")
            
            # You can replace this with your actual spell check model
            # For now, using a placeholder - replace with your model
            tokenizer = AutoTokenizer.from_pretrained(
                "bert-base-multilingual-cased",
                cache_dir="./cache"
            )
            
            # Placeholder model - replace with your actual spell check model
            model = AutoModelForTokenClassification.from_pretrained(
                "bert-base-multilingual-cased",
                num_labels=2,
                cache_dir="./cache"
            ).to(device)
            
            model.eval()
            SPELL_CHECK_MODEL["model"] = model
            SPELL_CHECK_MODEL["tokenizer"] = tokenizer
            print(f"✅ Khmer Spell Checker loaded successfully on {device}.")
            
        except Exception as e:
            print(f"❌ Failed to load spell checker: {e}")
            # Fallback to rule-based approach if model loading fails
            SPELL_CHECK_MODEL["model"] = "rule_based"
            SPELL_CHECK_MODEL["tokenizer"] = None

    return SPELL_CHECK_MODEL["model"], SPELL_CHECK_MODEL["tokenizer"]

# ================== Spell Checking Logic ==================
def khmer_spell_check(text):
    """
    Perform Khmer spell checking using model + rule-based approach
    Replace this with your actual model inference
    """
    try:
        model, tokenizer = load_spell_check_model()
        
        # If model loading failed, use rule-based approach
        if model == "rule_based":
            return rule_based_spell_check(text)
        
        # TODO: Replace with your actual model inference
        # This is a placeholder implementation
        corrected_text, errors, suggestions = advanced_spell_check(text)
        
        return {
            "corrected_text": corrected_text,
            "errors": errors,
            "suggestions": suggestions,
            "confidence": 0.85
        }
        
    except Exception as e:
        print(f"⚠️ Error in spell checking: {e}")
        # Fallback to rule-based approach
        return rule_based_spell_check(text)

def rule_based_spell_check(text):
    """Rule-based Khmer spell checking as fallback"""
    # Common Khmer spelling mistakes and corrections
    common_errors = {
        "អី": "អ្វី",
        "ហី": "ហេ",
        "មិគ": "មិន",
        "អាញ": "អាន",
        "ចង់": "ចង់",
        "រឺ": "ឬ",
        "នឹង": "នឹង",
        "ឯង": "ឯង"
    }
    
    errors = []
    suggestions = []
    corrected_text = text
    
    # Simple word-based correction
    words = text.split()
    for i, word in enumerate(words):
        if word in common_errors:
            errors.append({
                "word": word,
                "position": i,
                "suggestion": common_errors[word]
            })
            suggestions.append({
                "original": word,
                "corrected": common_errors[word],
                "context": " ".join(words[max(0, i-2):min(len(words), i+3)])
            })
            words[i] = common_errors[word]
    
    corrected_text = " ".join(words)
    
    return {
        "corrected_text": corrected_text,
        "errors": errors,
        "suggestions": suggestions,
        "confidence": 0.75
    }

def advanced_spell_check(text):
    """Advanced spell checking with your model"""
    # TODO: Implement your actual model inference here
    # This is a placeholder that simulates model output
    
    # Simulate processing delay
    import time
    time.sleep(0.5)
    
    # Simulate finding some errors
    errors = []
    suggestions = []
    corrected_text = text
    
    # Example: detect common issues
    if "អី" in text:
        errors.append({
            "word": "អី",
            "position": text.find("អី"),
            "suggestion": "អ្វី"
        })
        suggestions.append({
            "original": "អី",
            "corrected": "អ្វី", 
            "context": "Common colloquial form, standard is 'អ្វី'"
        })
        corrected_text = corrected_text.replace("អី", "អ្វី")
    
    return corrected_text, errors, suggestions

# ================== Summarization ==================
def summarize_text(input_text, model_key):
    """Summarize text using the selected model"""
    if not input_text.strip():
        return ""

    try:
        model, tokenizer = load_model(model_key)
        model_type = MODELS[model_key]["type"]

        # Tokenize input
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).to(device)

        # Generate summary
        with torch.no_grad():
            summary_ids = model.generate(
                **inputs,
                num_beams=4,
                max_new_tokens=125,
                early_stopping=True
            )

        # Decode output
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary.strip() or "មិនអាចសង្ខេបបានទេ។"

    except Exception as e:
        print(f"⚠️ Error summarizing with {model_key}: {e}")
        return f"កំហុស៖ {str(e)}"

# ================== Routes ==================
@app.route('/')
def front_page():
    """Front page with options to choose between spelling check and summarization"""
    return render_template('front_page.html')

@app.route('/spelling_check')
def spelling_check():
    """Khmer spelling check page"""
    return render_template('spelling_check.html')

@app.route('/summarize_page')
def summarize_page():
    """Main summarization page"""
    return render_template('index.html', models=MODELS)

@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    input_text = data.get("text", "").strip()
    selected_models = data.get("models", ["model1"])

    if not input_text:
        return jsonify({"error": "សូមបញ្ចូលអត្ថបទសិន។"}), 400

    results = {}
    for model_key in selected_models:
        if model_key in MODELS:
            results[model_key] = {
                "name": MODELS[model_key]["name"],
                "summary": summarize_text(input_text, model_key)
            }

    return jsonify({"results": results})

@app.route('/api/spell_check', methods=['POST'])
def spell_check():
    """Khmer spelling check API endpoint"""
    data = request.get_json()
    text = data.get("text", "").strip()
    
    if not text:
        return jsonify({"error": "សូមបញ្ចូលអត្ថបទសិន។"}), 400

    try:
        result = khmer_spell_check(text)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Spell check error: {e}")
        return jsonify({
            "corrected_text": text,
            "errors": [],
            "suggestions": [],
            "error": f"កំហុសក្នុងការត្រួតពិនិត្យអក្ខរាវិរុទ្ធ: {str(e)}"
        }), 500

@app.route('/get_models', methods=['GET'])
def get_models():
    """Return list of models to frontend"""
    return jsonify({
        key: {"name": value["name"]} for key, value in MODELS.items()
    })

# ================== Run ==================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
