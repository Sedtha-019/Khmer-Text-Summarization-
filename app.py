from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import torch
from peft import PeftModel
import warnings
from transformers import (
    MBartForConditionalGeneration, MBart50Tokenizer,
    MT5ForConditionalGeneration, T5Tokenizer
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
        "repo": "sedtha/mBart-50-large_LoRa_kh_sumerize",   # mBART model
        "type": "mbart",
        "model": None,
        "tokenizer": None
    },
    "model2": {
        "name": "Model 2 - Khmer mT5 Summarization",
        "repo": "angkor96/khmer-mT5-news-summarization",  # mT5 model
        "type": "mt5",
        "model": None,
        "tokenizer": None
    }
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

                # Load base mBART model
                base_model = MBartForConditionalGeneration.from_pretrained(
                    "facebook/mbart-large-50",
                    cache_dir="./cache"
                ).to(device)

                # Load LoRA adapter weights
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
                max_new_tokens=300,
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
def index():
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

@app.route('/summarize', methods=['POST'])
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

@app.route('/get_models', methods=['GET'])
def get_models():
    """Return list of models to frontend"""
    return jsonify({
        key: {"name": value["name"]} for key, value in MODELS.items()
    })

# ================== Run ==================
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
