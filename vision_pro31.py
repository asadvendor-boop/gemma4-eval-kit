#!/usr/bin/env python3
"""Vision test for Gemini 3.0 Flash only — using 10 correct images (8 programmatic + 2 real trilingual)."""

import os, json, time, base64
from pathlib import Path
from google import genai
from google.genai import types

GEMINI_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
IMG_DIR = Path(__file__).parent / "vision_test_results" / "images"
OUT_DIR = Path(__file__).parent / "vision_test_results"

_google = None
def get_google():
    global _google
    if _google is None:
        _google = genai.Client(api_key=GEMINI_API_KEY)
    return _google

def call_vision(image_path, question):
    client = get_google()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    ext = str(image_path).lower()
    mime = "image/jpeg" if ext.endswith('.jpg') or ext.endswith('.jpeg') else "image/png"
    
    img_part = types.Part.from_bytes(data=image_bytes, mime_type=mime)
    text_part = types.Part.from_text(text=question)
    contents = [types.Content(role="user", parts=[img_part, text_part])]
    config = types.GenerateContentConfig(
        temperature=0.0,
        max_output_tokens=4096,
        thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        http_options=types.HttpOptions(timeout=120_000),
    )
    full_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-3.1-pro-preview", contents=contents, config=config,
    ):
        if chunk.text:
            full_text += chunk.text
    return full_text or "(empty response)"

# 10 test images — same as other models
tests = [
    {"id": 1, "image": IMG_DIR / "01_bar_chart.png",
     "question": "Extract ALL numerical data from this bar chart. List each company's revenue for each quarter. Which company had the highest total annual revenue? Which had the highest growth rate Q1→Q4?",
     "keys": {"alpha_total":59,"beta_total":38,"gamma_total":86,"highest_total":"Gamma Ltd","alpha_growth":"50%","beta_growth":"25%","gamma_growth":"25%","highest_growth":"Alpha Corp"}},
    {"id": 2, "image": IMG_DIR / "02_pie_chart.png",
     "question": "What are the exact market share percentages for each company? Which company leads? What is the combined share of the top 3?",
     "keys": {"google":28.3,"apple":23.1,"samsung":19.7,"xiaomi":14.5,"others":14.4,"leader":"Google","top3_combined":71.1}},
    {"id": 3, "image": IMG_DIR / "03_data_table.png",
     "question": "Read this table. How many employees are in Engineering? Who has the highest salary? What is the average salary? Who was hired most recently?",
     "keys": {"engineering_count":3,"highest_salary_name":"Raj Patel","highest_salary_amount":"$142,000","average_salary":"$115,833","most_recent_hire":"Fatima Zahra","most_recent_date":"2023-01-08"}},
    {"id": 4, "image": IMG_DIR / "mix1.jpg",
     "question": "This image shows a vocabulary table with words in 3 languages: English, Urdu, and Arabic. Please read EVERY row carefully and output a structured table with all 3 columns (English, Urdu, Arabic) for each word. Also tell me: What is the title of this image? How many words are shown?",
     "keys": {"crawl":"Crawl","maize":"Maize","peasant":"Peasant","astounded":"Astounded","hammer":"Hammer","bend":"Bend"}},
    {"id": 5, "image": IMG_DIR / "05_line_chart.png",
     "question": "What was the stock price in January? In December? What two events are annotated on the chart? In which months did they occur? What is the overall percentage change from Jan to Dec?",
     "keys": {"jan_price":142,"dec_price":224,"event1":"Product Launch","event1_month":"May","event2":"CEO Resignation","event2_month":"September","pct_change":"57.7%"}},
    {"id": 6, "image": IMG_DIR / "06_math_equations.png",
     "question": "Read each equation. What is f(x)? What is f'(x)? What is the definite integral from 0 to 3? What is the sum of n² from 1 to 5? Are all calculations correct?",
     "keys": {"f_x":"3x","f_prime":"6x + 2","integral_result":15,"summation_result":55,"all_correct":True}},
    {"id": 7, "image": IMG_DIR / "07_code_bug.png",
     "question": "Read this Python code carefully. There is exactly ONE bug. What is the bug? What line is it on? What should the fix be? Will it cause an IndexError or wrong results?",
     "keys": {"bug_line":2,"bug_description":"len(arr) - 1","consequence":"IndexError"}},
    {"id": 8, "image": IMG_DIR / "08_mixed_lang.png",
     "question": "Read ALL text in this image. What are the 3 statistics shown (in both languages)? Where is the event located? What year?",
     "keys": {"attendees":"12,450","countries":"87","papers":"1,234","location":"Dubai","year":"2026","chinese_title":"全球人工智能大会"}},
    {"id": 9, "image": IMG_DIR / "09_scatter_trend.png",
     "question": "What is the equation of the trend line? What is the R² value? How many data points are plotted? What does the chart suggest about the relationship between study hours and exam scores?",
     "keys": {"slope":"2.0","n_points":10,"relationship":"positive"}},
    {"id": 10, "image": IMG_DIR / "mix2.jpg",
     "question": "This image shows a sentence translation table with sentences in English, Arabic, and Urdu. Please read EVERY row and output a structured table with all 3 columns. How many sentences are shown? Translate each Arabic and Urdu sentence back to English to verify accuracy.",
     "keys": {"tea":"tea","running":"running","forgive":"forgive","letter":"letter","food":"food"}},
]

print("="*60)
print("PRO 3.1 VISION TEST: 10 images")
print("="*60)

results = {}
for t in tests:
    print(f"\n  [Image {t['id']}] {t['image'].name}...", end=" ", flush=True)
    try:
        t0 = time.time()
        response = call_vision(t["image"], t["question"])
        elapsed = time.time() - t0
        results[t["id"]] = {"response": response, "elapsed": round(elapsed, 2), "chars": len(response)}
        print(f"✅ ({elapsed:.1f}s, {len(response)} chars)")
    except Exception as e:
        print(f"❌ {e}")
        results[t["id"]] = {"response": f"ERROR: {e}", "elapsed": 0, "chars": 0, "error": True}
    time.sleep(1)

# Save
out_path = OUT_DIR / "pro31_vision_results.json"
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\nResults saved to {out_path}")

# Print all responses
for t in tests:
    r = results.get(t["id"], {})
    resp = r.get("response", "")
    print(f"\n{'='*60}")
    print(f"[Image {t['id']}] {t['image'].name} ({r.get('elapsed',0)}s, {len(resp)} chars)")
    print(f"{'='*60}")
    print(resp[:800])
    if len(resp) > 800:
        print(f"... [{len(resp)-800} more chars]")
