#!/usr/bin/env python3
"""
VISION TEST: Generate 10 programmatic images with known ground truth,
send to all 4 models, evaluate responses against ground truth.

Images created with matplotlib + PIL so we know EXACTLY what's in each one.
"""

import os, sys, json, time, base64, io, traceback
from pathlib import Path
from datetime import datetime

# === Image generation ===
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# === API clients ===
from google import genai
from google.genai import types
from openai import OpenAI

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
GEMINI_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
DASHSCOPE_API_KEY = "YOUR_ALIBABA_DASHSCOPE_API_KEY"

MODELS = {
    "GEMMA4_MOE":  {"id": "gemma-4-26b-a4b-it",           "provider": "google"},
    "GEMMA4_31B":  {"id": "gemma-4-31b-it",                "provider": "google"},
    "FLASHLITE":   {"id": "gemini-3.1-flash-lite-preview", "provider": "google"},
    "QWEN35":      {"id": "qwen3.5-35b-a3b",              "provider": "qwen"},
}

OUT_DIR = Path(__file__).parent / "vision_test_results"
IMG_DIR = OUT_DIR / "images"
OUT_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# CLIENTS
# ---------------------------------------------------------------------------
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
        _qwen = OpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
    return _qwen

# ---------------------------------------------------------------------------
# IMAGE GENERATION — 10 images with known ground truth
# ---------------------------------------------------------------------------

def save_fig(fig, name):
    """Save matplotlib figure and return path."""
    path = IMG_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def save_pil(img, name):
    """Save PIL image and return path."""
    path = IMG_DIR / f"{name}.png"
    img.save(path)
    return path

def gen_image_1():
    """Bar chart: Q1-Q4 revenue for 3 companies."""
    fig, ax = plt.subplots(figsize=(10, 6))
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    alpha = [12, 15, 14, 18]  # Company Alpha
    beta = [8, 9, 11, 10]     # Company Beta
    gamma = [20, 19, 22, 25]  # Company Gamma

    x = np.arange(len(quarters))
    w = 0.25
    ax.bar(x - w, alpha, w, label='Alpha Corp', color='#2196F3')
    ax.bar(x, beta, w, label='Beta Inc', color='#FF9800')
    ax.bar(x + w, gamma, w, label='Gamma Ltd', color='#4CAF50')

    for i, v in enumerate(alpha): ax.text(i - w, v + 0.3, f'${v}M', ha='center', fontsize=8)
    for i, v in enumerate(beta):  ax.text(i, v + 0.3, f'${v}M', ha='center', fontsize=8)
    for i, v in enumerate(gamma): ax.text(i + w, v + 0.3, f'${v}M', ha='center', fontsize=8)

    ax.set_xlabel('Quarter')
    ax.set_ylabel('Revenue ($M)')
    ax.set_title('2025 Quarterly Revenue Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    ax.legend()
    ax.set_ylim(0, 30)

    return save_fig(fig, "01_bar_chart"), {
        "description": "Bar chart showing 2025 quarterly revenue for 3 companies",
        "data": {
            "Alpha Corp": {"Q1": 12, "Q2": 15, "Q3": 14, "Q4": 18},
            "Beta Inc":   {"Q1": 8,  "Q2": 9,  "Q3": 11, "Q4": 10},
            "Gamma Ltd":  {"Q1": 20, "Q2": 19, "Q3": 22, "Q4": 25},
        },
        "question": "Extract ALL numerical data from this bar chart. List each company's revenue for each quarter. Which company had the highest total annual revenue? Which had the highest growth rate Q1→Q4?",
        "answer_keys": {
            "alpha_total": 59,
            "beta_total": 38,
            "gamma_total": 86,
            "highest_total": "Gamma Ltd",
            "alpha_growth": "50%",
            "beta_growth": "25%",
            "gamma_growth": "25%",
            "highest_growth": "Alpha Corp",
        }
    }

def gen_image_2():
    """Pie chart: Market share."""
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = ['Google', 'Apple', 'Samsung', 'Xiaomi', 'Others']
    sizes = [28.3, 23.1, 19.7, 14.5, 14.4]
    colors = ['#4285F4', '#A2AAAD', '#1428A0', '#FF6900', '#CCCCCC']
    explode = (0.05, 0, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Global Smartphone Market Share Q1 2026')

    return save_fig(fig, "02_pie_chart"), {
        "description": "Pie chart showing smartphone market share Q1 2026",
        "question": "What are the exact market share percentages for each company? Which company leads? What is the combined share of the top 3?",
        "answer_keys": {
            "google": 28.3,
            "apple": 23.1,
            "samsung": 19.7,
            "xiaomi": 14.5,
            "others": 14.4,
            "leader": "Google",
            "top3_combined": 71.1,
        }
    }

def gen_image_3():
    """Data table: Employee records."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')

    data = [
        ['001', 'Ahmad Khan',    'Engineering', '$125,000', '2021-03-15'],
        ['002', 'Sarah Chen',    'Marketing',   '$95,000',  '2022-07-01'],
        ['003', 'Olga Petrov',   'Finance',     '$110,000', '2020-11-22'],
        ['004', 'James Wilson',  'Engineering', '$135,000', '2019-05-10'],
        ['005', 'Fatima Zahra',  'HR',          '$88,000',  '2023-01-08'],
        ['006', 'Raj Patel',     'Engineering', '$142,000', '2018-09-30'],
    ]
    cols = ['ID', 'Name', 'Department', 'Salary', 'Hire Date']

    table = ax.table(cellText=data, colLabels=cols, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    for j in range(len(cols)):
        table[0, j].set_facecolor('#2196F3')
        table[0, j].set_text_props(color='white', fontweight='bold')

    ax.set_title('Employee Directory — TechCorp 2026', fontsize=14, pad=20)

    return save_fig(fig, "03_data_table"), {
        "description": "Employee data table with 6 rows",
        "question": "Read this table. How many employees are in Engineering? Who has the highest salary? What is the average salary? Who was hired most recently?",
        "answer_keys": {
            "engineering_count": 3,
            "highest_salary_name": "Raj Patel",
            "highest_salary_amount": "$142,000",
            "average_salary": "$115,833",
            "most_recent_hire": "Fatima Zahra",
            "most_recent_date": "2023-01-08",
        }
    }

def gen_image_4():
    """Arabic text — a known paragraph."""
    img = Image.new('RGB', (800, 300), 'white')
    draw = ImageDraw.Draw(img)
    
    # Use a system font that supports Arabic
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 28)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 18)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/GeezaPro.ttc", 28)
            small = ImageFont.truetype("/System/Library/Fonts/GeezaPro.ttc", 18)
        except:
            font = ImageFont.load_default()
            small = font

    title = "بسم الله الرحمن الرحيم"
    line1 = "الذكاء الاصطناعي هو مستقبل التكنولوجيا"
    line2 = "تأسست شركة جوجل في عام ١٩٩٨"
    line3 = "عدد الموظفين: ١٨٢,٥٠٢"

    draw.text((400, 30), title, font=font, fill='#1a237e', anchor='mt')
    draw.text((400, 90), line1, font=small, fill='black', anchor='mt')
    draw.text((400, 130), line2, font=small, fill='black', anchor='mt')
    draw.text((400, 170), line3, font=small, fill='#d32f2f', anchor='mt')
    draw.text((400, 230), "— صفحة ١ من ٣ —", font=small, fill='gray', anchor='mt')

    return save_pil(img, "04_arabic_text"), {
        "description": "Arabic text with specific claims",
        "question": "Read and translate ALL Arabic text in this image to English. What year is mentioned? What number of employees is stated? What page number is shown?",
        "answer_keys": {
            "bismillah": "In the name of God, the Most Gracious, the Most Merciful",
            "line1_meaning": "Artificial intelligence is the future of technology",
            "year_mentioned": "1998",
            "employee_count": "182,502",
            "page_number": "Page 1 of 3",
        }
    }

def gen_image_5():
    """Line chart with annotations — stock price."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    prices = [142, 155, 148, 162, 175, 168, 183, 195, 188, 201, 210, 224]
    
    ax.plot(months, prices, 'b-o', linewidth=2, markersize=6)
    
    # Annotations
    ax.annotate('Product Launch', xy=(4, 175), xytext=(4, 190),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=10, color='green', fontweight='bold')
    ax.annotate('CEO Resignation', xy=(8, 188), xytext=(8, 170),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red', fontweight='bold')
    
    ax.set_xlabel('Month (2025)')
    ax.set_ylabel('Stock Price ($)')
    ax.set_title('ACME Corp (ACME) — 2025 Stock Performance')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(130, 240)

    return save_fig(fig, "05_line_chart"), {
        "description": "Stock price line chart with 2 annotations",
        "question": "What was the stock price in January? In December? What two events are annotated on the chart? In which months did they occur? What is the overall percentage change from Jan to Dec?",
        "answer_keys": {
            "jan_price": 142,
            "dec_price": 224,
            "event1": "Product Launch",
            "event1_month": "May",
            "event2": "CEO Resignation",
            "event2_month": "September",
            "pct_change": "57.7%",
        }
    }

def gen_image_6():
    """Math equations — handwritten style."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    equations = [
        (r'$f(x) = 3x^2 + 2x - 7$', 0.85),
        (r"$f'(x) = 6x + 2$", 0.70),
        (r'$\int_0^3 f(x)\,dx = \left[x^3 + x^2 - 7x\right]_0^3$', 0.50),
        (r'$= (27 + 9 - 21) - (0) = 15$', 0.35),
        (r'$\sum_{n=1}^{5} n^2 = 1 + 4 + 9 + 16 + 25 = 55$', 0.15),
    ]
    
    ax.set_title('Mathematics Worksheet', fontsize=16, pad=20)
    for eq, y in equations:
        ax.text(0.5, y, eq, fontsize=18, ha='center', transform=ax.transAxes)

    return save_fig(fig, "06_math_equations"), {
        "description": "Math worksheet with function, derivative, integral, and summation",
        "question": "Read each equation. What is f(x)? What is f'(x)? What is the definite integral from 0 to 3? What is the sum of n² from 1 to 5? Are all calculations correct?",
        "answer_keys": {
            "f_x": "3x² + 2x - 7",
            "f_prime": "6x + 2",
            "integral_result": 15,
            "summation_result": 55,
            "all_correct": True,
        }
    }

def gen_image_7():
    """Code screenshot with a deliberate bug."""
    img = Image.new('RGB', (700, 400), '#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    except:
        font = ImageFont.load_default()
    
    lines = [
        ("def binary_search(arr, target):", '#569CD6'),
        ("    low, high = 0, len(arr)", '#FFFFFF'),       # BUG: should be len(arr) - 1
        ("    while low <= high:", '#FFFFFF'),
        ("        mid = (low + high) // 2", '#FFFFFF'),
        ("        if arr[mid] == target:", '#FFFFFF'),
        ("            return mid", '#FFFFFF'),
        ("        elif arr[mid] < target:", '#FFFFFF'),
        ("            low = mid + 1", '#FFFFFF'),
        ("        else:", '#FFFFFF'),
        ("            high = mid - 1", '#FFFFFF'),
        ("    return -1", '#FFFFFF'),
        ("", '#FFFFFF'),
        ("# Test", '#6A9955'),
        ("result = binary_search([1,3,5,7,9], 7)", '#FFFFFF'),
        ("print(result)  # Expected: 3", '#6A9955'),
    ]
    
    y = 15
    for i, (line, color) in enumerate(lines):
        # Line numbers
        draw.text((10, y), f"{i+1:2d}", font=font, fill='#858585')
        draw.text((40, y), line, font=font, fill=color)
        y += 24
    
    # Title bar
    draw.rectangle([(0, 0), (700, 10)], fill='#323233')

    return save_pil(img, "07_code_bug"), {
        "description": "Python binary search code with a deliberate bug",
        "question": "Read this Python code carefully. There is exactly ONE bug. What is the bug? What line is it on? What should the fix be? Will it cause an IndexError or wrong results?",
        "answer_keys": {
            "bug_line": 2,
            "bug_description": "high = len(arr) should be high = len(arr) - 1",
            "consequence": "IndexError (array index out of bounds)",
        }
    }

def gen_image_8():
    """Mixed language: English + Chinese + numbers."""
    img = Image.new('RGB', (800, 400), '#f5f5f5')
    draw = ImageDraw.Draw(img)
    
    try:
        font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 24)
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 18)
    except:
        font_lg = ImageFont.load_default()
        font_sm = font_lg
    
    draw.rectangle([(20, 20), (780, 380)], outline='#333', width=2)
    
    draw.text((400, 40), "Global AI Conference 2026", font=font_lg, fill='#1a237e', anchor='mt')
    draw.text((400, 80), "全球人工智能大会 2026", font=font_lg, fill='#1a237e', anchor='mt')
    
    draw.text((60, 130), "• Attendees: 12,450", font=font_sm, fill='black')
    draw.text((60, 160), "• 参会人数：12,450人", font=font_sm, fill='black')
    draw.text((60, 200), "• Countries: 87", font=font_sm, fill='black')
    draw.text((60, 230), "• 参与国家：87个", font=font_sm, fill='black')
    draw.text((60, 270), "• Papers: 1,234", font=font_sm, fill='black')
    draw.text((60, 300), "• 论文数量：1,234篇", font=font_sm, fill='black')
    
    draw.text((400, 360), "Location: Dubai, UAE / 地点：迪拜，阿联酋", font=font_sm, fill='gray', anchor='mt')

    return save_pil(img, "08_mixed_lang"), {
        "description": "Bilingual English-Chinese conference poster with statistics",
        "question": "Read ALL text in this image. What are the 3 statistics shown (in both languages)? Where is the event located? What year?",
        "answer_keys": {
            "attendees": "12,450",
            "countries": "87",
            "papers": "1,234",
            "location": "Dubai, UAE",
            "year": "2026",
            "chinese_title": "全球人工智能大会",
        }
    }

def gen_image_9():
    """Scatter plot with trend line and R² value."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    np.random.seed(42)
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([2.1, 4.3, 5.8, 8.2, 9.5, 12.1, 13.8, 16.0, 17.5, 20.2])
    
    ax.scatter(x, y, color='#E91E63', s=80, zorder=5, label='Data Points')
    
    # Trend line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), 'b--', linewidth=2, label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    # R² calculation
    yhat = p(x)
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot
    
    ax.text(2, 18, f'R² = {r2:.4f}', fontsize=14, 
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray'))
    ax.text(2, 16, f'n = {len(x)}', fontsize=12, color='gray')
    
    ax.set_xlabel('Study Hours per Day')
    ax.set_ylabel('Exam Score')
    ax.set_title('Study Hours vs Exam Performance')
    ax.legend()
    ax.grid(True, alpha=0.3)

    return save_fig(fig, "09_scatter_trend"), {
        "description": "Scatter plot with linear regression trend line and R² value",
        "question": "What is the equation of the trend line? What is the R² value? How many data points are plotted? What does the chart suggest about the relationship between study hours and exam scores?",
        "answer_keys": {
            "slope": round(z[0], 2),
            "intercept": round(z[1], 2),
            "r_squared": round(r2, 4),
            "n_points": 10,
            "relationship": "strong positive linear correlation",
        }
    }

def gen_image_10():
    """Urdu text — technical content."""
    img = Image.new('RGB', (800, 350), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 22)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 16)
    except:
        font = ImageFont.load_default()
        small = font

    draw.text((400, 25), "اردو ٹیکنالوجی بلیٹن", font=font, fill='#0d47a1', anchor='mt')
    draw.text((400, 70), "تاریخ: ۲ اپریل ۲۰۲۶", font=small, fill='gray', anchor='mt')
    draw.text((400, 110), "جیما ۴ ماڈل ۲۶ ارب پیرامیٹرز پر مشتمل ہے", font=small, fill='black', anchor='mt')
    draw.text((400, 145), "اس میں صرف ۴ ارب پیرامیٹرز فعال ہیں", font=small, fill='black', anchor='mt')
    draw.text((400, 185), "رفتار: ۳۶۳ ٹوکنز فی سیکنڈ", font=small, fill='#d32f2f', anchor='mt')
    draw.text((400, 225), "لائسنس: اپاچی ۲.۰", font=small, fill='#2e7d32', anchor='mt')
    draw.text((400, 270), "قیمت: مفت اور اوپن سورس", font=small, fill='#2e7d32', anchor='mt')

    return save_pil(img, "10_urdu_text"), {
        "description": "Urdu technology bulletin about Gemma 4",
        "question": "Read and translate ALL Urdu text in this image. What model is discussed? How many total parameters? How many active? What speed? What license? Is it free?",
        "answer_keys": {
            "model": "Gemma 4",
            "total_params": "26 billion",
            "active_params": "4 billion",
            "speed": "363 tokens per second",
            "license": "Apache 2.0",
            "free": True,
            "date": "2 April 2026",
        }
    }


# ---------------------------------------------------------------------------
# API CALL WITH IMAGE
# ---------------------------------------------------------------------------
def call_google_vision(model_id, image_path, question):
    """Send image + question to a Google model."""
    client = get_google()
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    img_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
    text_part = types.Part.from_text(text=question)
    
    contents = [types.Content(role="user", parts=[img_part, text_part])]
    config = types.GenerateContentConfig(
        temperature=0.0,
        max_output_tokens=4096,
        http_options=types.HttpOptions(timeout=120_000),
    )
    
    full_text = ""
    for chunk in client.models.generate_content_stream(
        model=model_id, contents=contents, config=config,
    ):
        if chunk.text:
            full_text += chunk.text
    return full_text or "(empty response)"


def call_qwen_vision(image_path, question):
    """Send image + question to Qwen via OpenAI-compatible API."""
    client = get_qwen()
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            {"type": "text", "text": question},
        ]
    }]
    
    completion = client.chat.completions.create(
        model="qwen3.5-35b-a3b",
        messages=messages,
        temperature=0.0,
        max_tokens=4096,
        extra_body={"enable_thinking": False},
        timeout=120,
    )
    return completion.choices[0].message.content or "(empty response)"


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    print("="*70)
    print("VISION TEST: 10 images × 4 models = 40 evaluations")
    print("="*70)
    
    # Step 1: Generate all 10 images
    print("\n[1/3] Generating test images...")
    generators = [
        gen_image_1, gen_image_2, gen_image_3, gen_image_4, gen_image_5,
        gen_image_6, gen_image_7, gen_image_8, gen_image_9, gen_image_10,
    ]
    
    test_cases = []
    for i, gen_fn in enumerate(generators):
        path, ground_truth = gen_fn()
        test_cases.append({
            "id": i + 1,
            "image_path": str(path),
            "description": ground_truth["description"],
            "question": ground_truth["question"],
            "answer_keys": ground_truth["answer_keys"],
        })
        print(f"  ✅ Image {i+1}: {ground_truth['description']}")
    
    # Save ground truth
    gt_path = OUT_DIR / "ground_truth.json"
    with open(gt_path, 'w') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
    print(f"\n  Ground truth saved to {gt_path}")
    
    # Step 2: Send to all models
    print("\n[2/3] Sending images to models...")
    results = {}
    
    model_order = ["GEMMA4_MOE", "GEMMA4_31B", "FLASHLITE", "QWEN35"]
    
    # Check for existing results (resume capability)
    results_path = OUT_DIR / "results.json"
    if results_path.exists():
        results = json.loads(results_path.read_text())
        print(f"  Loaded {len(results)} existing results")
    
    for model_key in model_order:
        model_info = MODELS[model_key]
        print(f"\n{'='*50}")
        print(f"  Model: {model_key} ({model_info['id']})")
        print(f"{'='*50}")
        
        for tc in test_cases:
            rkey = f"{model_key}::{tc['id']}"
            if rkey in results:
                print(f"  [Image {tc['id']}] CACHED — skipping")
                continue
            
            print(f"  [Image {tc['id']}] {tc['description']}...", end=" ", flush=True)
            
            try:
                t0 = time.time()
                if model_info["provider"] == "google":
                    response = call_google_vision(model_info["id"], tc["image_path"], tc["question"])
                else:
                    response = call_qwen_vision(tc["image_path"], tc["question"])
                elapsed = time.time() - t0
                
                results[rkey] = {
                    "model": model_key,
                    "image_id": tc["id"],
                    "response": response,
                    "elapsed": round(elapsed, 2),
                    "chars": len(response),
                }
                print(f"✅ ({elapsed:.1f}s, {len(response)} chars)")
                
                # Save after every response
                results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
                
            except Exception as e:
                print(f"❌ {e}")
                results[rkey] = {
                    "model": model_key,
                    "image_id": tc["id"],
                    "response": f"ERROR: {str(e)}",
                    "elapsed": 0,
                    "chars": 0,
                    "error": True,
                }
                results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
                time.sleep(5)
    
    # Save final results
    results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Step 3: Score results
    print("\n[3/3] SCORING...")
    score_results(test_cases, results, model_order)


def score_results(test_cases, results, model_order):
    """Score each model's response against ground truth."""
    
    scores = {m: [] for m in model_order}
    
    for tc in test_cases:
        print(f"\n{'='*60}")
        print(f"Image {tc['id']}: {tc['description']}")
        print(f"{'='*60}")
        
        for model_key in model_order:
            rkey = f"{model_key}::{tc['id']}"
            result = results.get(rkey, {})
            response = result.get("response", "")
            
            if result.get("error"):
                print(f"  [{model_key}] ❌ ERROR — score 0")
                scores[model_key].append(0)
                continue
            
            # Generic scoring: check how many answer_keys appear in response
            response_lower = response.lower()
            found = 0
            total = len(tc["answer_keys"])
            
            for key, expected in tc["answer_keys"].items():
                expected_str = str(expected).lower()
                
                # Flexible matching
                if expected_str in response_lower:
                    found += 1
                elif isinstance(expected, (int, float)):
                    # Try with commas, without, etc.
                    if str(expected) in response or f"{expected:,}" in response:
                        found += 1
                    elif isinstance(expected, float):
                        # Try rounded versions
                        if f"{expected:.1f}" in response or f"{expected:.2f}" in response:
                            found += 1
                elif isinstance(expected, bool):
                    if expected and ("yes" in response_lower or "correct" in response_lower or "true" in response_lower):
                        found += 1
                    elif not expected and ("no" in response_lower or "incorrect" in response_lower or "false" in response_lower):
                        found += 1
            
            pct = found / total if total > 0 else 0
            score = round(pct * 10, 1)
            scores[model_key].append(score)
            
            status = "✅" if pct >= 0.7 else "⚠️" if pct >= 0.4 else "❌"
            print(f"  [{model_key}] {status} {found}/{total} keys found — score {score}/10")
    
    # Final summary
    print(f"\n{'='*60}")
    print("VISION TEST FINAL SCORES")
    print(f"{'='*60}")
    
    for model_key in model_order:
        s = scores[model_key]
        avg = sum(s) / len(s) if s else 0
        print(f"\n  [{model_key}]")
        for i, sc in enumerate(s):
            print(f"    Image {i+1}: {sc}/10")
        print(f"    AVERAGE: {avg:.2f}/10")


if __name__ == "__main__":
    main()
