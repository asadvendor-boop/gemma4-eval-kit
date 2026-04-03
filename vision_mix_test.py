#!/usr/bin/env python3
"""Send mix1.jpg and mix2.jpg to all 4 models for trilingual OCR evaluation."""

import os, sys, json, time, base64
from pathlib import Path
from google import genai
from google.genai import types
from openai import OpenAI

GEMINI_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
DASHSCOPE_API_KEY = "YOUR_ALIBABA_DASHSCOPE_API_KEY"

MODELS = {
    "GEMMA4_MOE":  {"id": "gemma-4-26b-a4b-it",           "provider": "google"},
    "GEMMA4_31B":  {"id": "gemma-4-31b-it",                "provider": "google"},
    "FLASHLITE":   {"id": "gemini-3.1-flash-lite-preview", "provider": "google"},
    "QWEN35":      {"id": "qwen3.5-35b-a3b",              "provider": "qwen"},
}

IMG_DIR = Path(__file__).parent / "vision_test_results" / "images"

_google = None
_qwen = None

def get_google():
    global _google
    if _google is None:
        _google = genai.Client(api_key=GEMINI_API_KEY)
    return _google

def get_qwen():
    global _qwen
    if _qwen is None:
        _qwen = OpenAI(api_key=DASHSCOPE_API_KEY, base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
    return _qwen

def call_google_vision(model_id, image_path, question):
    client = get_google()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    mime = "image/jpeg" if str(image_path).endswith('.jpg') else "image/png"
    img_part = types.Part.from_bytes(data=image_bytes, mime_type=mime)
    text_part = types.Part.from_text(text=question)
    contents = [types.Content(role="user", parts=[img_part, text_part])]
    config = types.GenerateContentConfig(
        temperature=0.0, max_output_tokens=4096,
        http_options=types.HttpOptions(timeout=120_000),
    )
    full_text = ""
    for chunk in client.models.generate_content_stream(model=model_id, contents=contents, config=config):
        if chunk.text:
            full_text += chunk.text
    return full_text or "(empty response)"

def call_qwen_vision(image_path, question):
    client = get_qwen()
    with open(image_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    mime = "image/jpeg" if str(image_path).endswith('.jpg') else "image/png"
    messages = [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        {"type": "text", "text": question},
    ]}]
    completion = client.chat.completions.create(
        model="qwen3.5-35b-a3b", messages=messages,
        temperature=0.0, max_tokens=4096,
        extra_body={"enable_thinking": False}, timeout=120,
    )
    return completion.choices[0].message.content or "(empty response)"


# ============================================================
# TEST DEFINITIONS
# ============================================================
tests = [
    {
        "id": "mix1",
        "image": IMG_DIR / "mix1.jpg",
        "question": "This image shows a vocabulary table with words in 3 languages: English, Urdu, and Arabic. Please read EVERY row carefully and output a structured table with all 3 columns (English, Urdu, Arabic) for each word. Also tell me: What is the title of this image? How many words are shown?",
        "ground_truth": {
            "title": "1000 Arabic Words in English and Urdu Part 11",
            "word_count": 6,
            "words": [
                {"english": "Crawl", "urdu": "رینگنا", "arabic": "زَحْفُ"},
                {"english": "Maize", "urdu": "مکی", "arabic": "ذُرَّةٌ"},
                {"english": "Peasant", "urdu": "کسان", "arabic": "مُزَارِعُ"},
                {"english": "Astounded", "urdu": "ہکابکا", "arabic": "حَيْرَانُ"},
                {"english": "Hammer", "urdu": "ہتھوڑا", "arabic": "مِطْرَقَةٌ"},
                {"english": "Bend", "urdu": "جھکنا", "arabic": "خُضُوعٌ"},
            ]
        }
    },
    {
        "id": "mix2",
        "image": IMG_DIR / "mix2.jpg",
        "question": "This image shows a sentence translation table with sentences in English, Arabic, and Urdu. Please read EVERY row and output a structured table with all 3 columns. How many sentences are shown? Translate each Arabic and Urdu sentence back to English to verify accuracy.",
        "ground_truth": {
            "sentence_count": 5,
            "sentences": [
                {"english": "He was taking tea", "arabic": "كَانَ يَشْرُبُ الشَّايَ", "urdu": "وہ چائے پی رہا تھا"},
                {"english": "He is running", "arabic": "هُوَ يَهْرُبُ", "urdu": "وہ دوڑ رہا ہے"},
                {"english": "Please forgive her", "arabic": "بِفَضْلِكَ أَنْ تُسَامِحَهَا", "urdu": "براۓ مہربانی سے معاف کردیں"},
                {"english": "He wrote a letter", "arabic": "كَتَبَ رِسَالَةً", "urdu": "اس نے ایک خط لکھا"},
                {"english": "She cooked food", "arabic": "اِنَّهَا طَبَخَتِ الطَّعَامَ", "urdu": "اس نے کھانا پکایا"},
            ]
        }
    },
]

# ============================================================
# RUN
# ============================================================
model_order = ["GEMMA4_MOE", "GEMMA4_31B", "FLASHLITE", "QWEN35"]
results = {}

print("="*70)
print("TRILINGUAL VISION TEST: 2 real images × 4 models")
print("="*70)

for test in tests:
    print(f"\n{'='*60}")
    print(f"Image: {test['id']} — {test['image'].name}")
    print(f"{'='*60}")
    
    for model_key in model_order:
        model_info = MODELS[model_key]
        rkey = f"{model_key}::{test['id']}"
        
        print(f"  [{model_key}] Sending... ", end="", flush=True)
        try:
            t0 = time.time()
            if model_info["provider"] == "google":
                response = call_google_vision(model_info["id"], test["image"], test["question"])
            else:
                response = call_qwen_vision(test["image"], test["question"])
            elapsed = time.time() - t0
            
            results[rkey] = {
                "model": model_key,
                "test_id": test["id"],
                "response": response,
                "elapsed": round(elapsed, 2),
                "chars": len(response),
            }
            print(f"✅ ({elapsed:.1f}s, {len(response)} chars)")
            
        except Exception as e:
            elapsed = time.time() - t0
            print(f"❌ {e}")
            results[rkey] = {
                "model": model_key,
                "test_id": test["id"],
                "response": f"ERROR: {str(e)}",
                "elapsed": round(elapsed, 2),
                "chars": 0,
                "error": True,
            }
        
        time.sleep(1)

# Save results
out_path = Path(__file__).parent / "vision_test_results" / "mix_results.json"
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\nResults saved to {out_path}")

# ============================================================
# PRINT RESPONSES FOR EVALUATION
# ============================================================
print(f"\n{'='*70}")
print("FULL RESPONSES")
print(f"{'='*70}")

for test in tests:
    for model_key in model_order:
        rkey = f"{model_key}::{test['id']}"
        r = results.get(rkey, {})
        resp = r.get("response", "")
        print(f"\n{'='*60}")
        print(f"[{model_key}] {test['id']} ({r.get('elapsed',0)}s, {len(resp)} chars)")
        print(f"{'='*60}")
        print(resp[:1500])
        if len(resp) > 1500:
            print(f"... [{len(resp)-1500} more chars]")
