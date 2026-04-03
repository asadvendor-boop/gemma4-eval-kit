#!/usr/bin/env python3
"""
Gemma 4 vs Qwen 3.5 vs Flash Lite — 60-Test Evaluation Runner
Fault-tolerant with resume capability. Saves progress after every test.
"""

import os, sys, time, json, traceback
from datetime import datetime
from pathlib import Path

# === Install: pip install google-genai openai ===
from google import genai
from google.genai import types
from openai import OpenAI

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
GEMINI_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
DASHSCOPE_API_KEY = "YOUR_ALIBABA_DASHSCOPE_API_KEY"

MODELS = {
    "gemma4":      {"id": "gemma-4-26b-a4b-it",              "provider": "google", "thinking": "MINIMAL"},
    "gemma4_31b":  {"id": "gemma-4-31b-it",                  "provider": "google", "thinking": "MINIMAL"},
    "flashlite":   {"id": "gemini-3.1-flash-lite-preview",    "provider": "google", "thinking": "MINIMAL"},
    "flash3":      {"id": "gemini-3-flash-preview",           "provider": "google", "thinking": "MINIMAL"},
    "pro31":       {"id": "gemini-3.1-pro-preview",           "provider": "google", "thinking": "LOW"},
    "qwen35":      {"id": "qwen3.5-35b-a3b",                 "provider": "qwen",   "thinking": None},
}

BASE_DIR  = Path(__file__).parent
OUT_DIR   = BASE_DIR / "eval_results"
PROGRESS  = OUT_DIR / "progress.json"
MAX_RETRIES = 5
RETRY_BASE_DELAY = 10  # seconds, doubles each retry

# ---------------------------------------------------------------------------
# CLIENTS (lazy init to survive import-time network issues)
# ---------------------------------------------------------------------------
_google = None
_qwen   = None

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
# PROGRESS MANAGEMENT
# ---------------------------------------------------------------------------
def load_progress():
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text())
    return {}

def save_progress(prog):
    PROGRESS.write_text(json.dumps(prog, indent=2, ensure_ascii=False))

def result_key(test_id, model_key):
    return f"{test_id}::{model_key}"

# ---------------------------------------------------------------------------
# API CALLERS  (single-turn)
# ---------------------------------------------------------------------------
def call_google_single(model_id, prompt, system_prompt=None, temperature=0.0, thinking_level="MINIMAL"):
    client = get_google()
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    cfg_kwargs = {
        "temperature": temperature,
        "top_p": 1,
        "max_output_tokens": 8192,
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
        "http_options": types.HttpOptions(timeout=300_000),
    }
    if system_prompt:
        cfg_kwargs["system_instruction"] = system_prompt
    config = types.GenerateContentConfig(**cfg_kwargs)

    # Use non-streaming for models with thinking (Pro) to avoid hanging on thought chunks
    if thinking_level in ("LOW", "MEDIUM", "HIGH"):
        resp = client.models.generate_content(
            model=model_id, contents=contents, config=config,
        )
        text = resp.text or "(empty response)"
        print(f"\n{text[:200]}...")
        return text
    else:
        full_text = ""
        print()  # newline before streaming output
        for chunk in client.models.generate_content_stream(
            model=model_id, contents=contents, config=config,
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text += chunk.text
        print()  # newline after
        return full_text or "(empty response)"


def call_qwen_single(prompt, system_prompt=None, temperature=0.0):
    client = get_qwen()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="qwen3.5-35b-a3b",
        messages=messages,
        temperature=temperature,
        top_p=1.0 if temperature == 0 else 0.8,
        max_tokens=8192,
        extra_body={"enable_thinking": False, "result_format": "message"},
        timeout=120,
    )
    content = completion.choices[0].message.content
    return content or "(empty response)"

# ---------------------------------------------------------------------------
# API CALLERS  (multi-turn)
# ---------------------------------------------------------------------------
def call_google_multi(model_id, turns, system_prompt=None, temperature=0.0, thinking_level="MINIMAL"):
    """turns = list of user prompt strings. Returns list of model responses."""
    client = get_google()
    cfg_kwargs = {
        "temperature": temperature,
        "max_output_tokens": 8192,
        "thinking_config": types.ThinkingConfig(thinking_level=thinking_level),
        "http_options": types.HttpOptions(timeout=300_000),
    }
    if system_prompt:
        cfg_kwargs["system_instruction"] = system_prompt
    config = types.GenerateContentConfig(**cfg_kwargs)

    conversation = []
    responses = []
    for turn_idx, user_msg in enumerate(turns, 1):
        conversation.append(types.Content(role="user", parts=[types.Part.from_text(text=user_msg)]))
        print(f"\n      [Turn {turn_idx}] ", end="", flush=True)
        if thinking_level in ("LOW", "MEDIUM", "HIGH"):
            resp = client.models.generate_content(
                model=model_id, contents=conversation, config=config,
            )
            txt = resp.text or "(empty)"
            print(txt[:200])
        else:
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model=model_id, contents=conversation, config=config,
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_text += chunk.text
            print()
            txt = full_text or "(empty)"
        responses.append(txt)
        conversation.append(types.Content(role="model", parts=[types.Part.from_text(text=txt)]))
    return responses


def call_qwen_multi(turns, system_prompt=None, temperature=0.0):
    client = get_qwen()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    responses = []
    for user_msg in turns:
        messages.append({"role": "user", "content": user_msg})
        completion = client.chat.completions.create(
            model="qwen3.5-35b-a3b",
            messages=messages,
            temperature=temperature,
            top_p=1.0 if temperature == 0 else 0.8,
            max_tokens=8192,
            extra_body={"enable_thinking": False, "result_format": "message"},
            timeout=120,
        )
        txt = completion.choices[0].message.content or "(empty)"
        responses.append(txt)
        messages.append({"role": "assistant", "content": txt})
    return responses

# ---------------------------------------------------------------------------
# UNIFIED DISPATCHER  (with retries + backoff)
# ---------------------------------------------------------------------------
def run_single(model_key, prompt, system_prompt=None, temperature=0.0):
    info = MODELS[model_key]
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if info["provider"] == "google":
                return call_google_single(info["id"], prompt, system_prompt, temperature, thinking_level=info.get("thinking", "MINIMAL"))
            else:
                return call_qwen_single(prompt, system_prompt, temperature)
        except Exception as e:
            delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
            print(f"      ⚠ Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"        Retrying in {delay}s …")
                time.sleep(delay)
            else:
                return f"[ERROR after {MAX_RETRIES} retries]: {e}"


def run_multi(model_key, turns, system_prompt=None, temperature=0.0):
    info = MODELS[model_key]
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if info["provider"] == "google":
                return call_google_multi(info["id"], turns, system_prompt, temperature, thinking_level=info.get("thinking", "MINIMAL"))
            else:
                return call_qwen_multi(turns, system_prompt, temperature)
        except Exception as e:
            delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
            print(f"      ⚠ Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"        Retrying in {delay}s …")
                time.sleep(delay)
            else:
                return [f"[ERROR after {MAX_RETRIES} retries]: {e}"]

# ---------------------------------------------------------------------------
# RESULT WRITER
# ---------------------------------------------------------------------------
def write_result(model_key, test, response_text, elapsed):
    fpath = OUT_DIR / f"{model_key}_results.txt"
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"TEST {test['id']}: {test['name']}\n")
        f.write(f"CATEGORY: {test['cat']}\n")
        f.write(f"TEMPERATURE: {test['temp']}\n")
        f.write(f"TIME: {elapsed:.1f}s\n")
        f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
        f.write(f"{'='*70}\n\n")
        f.write(response_text)
        f.write(f"\n\n{'─'*70}\n")

# ---------------------------------------------------------------------------
# MAIN RUNNER
# ---------------------------------------------------------------------------
def run_all():
    # Import tests from both parts
    from eval_tests_part1 import TESTS_PART1
    from eval_tests_part2 import TESTS_PART2
    ALL_TESTS = TESTS_PART1 + TESTS_PART2

    OUT_DIR.mkdir(exist_ok=True)
    progress = load_progress()

    total = len(ALL_TESTS) * len(MODELS)
    done  = sum(1 for t in ALL_TESTS for m in MODELS if result_key(t["id"], m) in progress)

    print(f"\n🧪 GEMMA 4 EVALUATION — {len(ALL_TESTS)} tests × {len(MODELS)} models = {total} runs")
    print(f"   Already completed: {done}/{total}")
    if done == total:
        print("   ✅ All tests already finished! Delete progress.json to re-run.")
        return
    print(f"   Results → {OUT_DIR.resolve()}\n")

    model_order = ["pro31"]  # Only run the new model
    completed = done

    for test in ALL_TESTS:
        for mk in model_order:
            rk = result_key(test["id"], mk)
            if rk in progress:
                continue  # already done — resume past this

            completed += 1
            label = f"[{completed}/{total}] Test {test['id']} ({test['cat']}) → {mk}"
            print(f"  🔄 {label} …", end="", flush=True)

            t0 = time.time()

            # --- dispatch ---
            if test.get("turns"):
                # multi-turn test
                resp_list = run_multi(mk, test["turns"],
                                      system_prompt=test.get("system"),
                                      temperature=test["temp"])
                response_text = ""
                for i, r in enumerate(resp_list, 1):
                    response_text += f"\n--- TURN {i} RESPONSE ---\n{r}\n"
            else:
                # single-turn
                response_text = run_single(mk, test["prompt"],
                                           system_prompt=test.get("system"),
                                           temperature=test["temp"])

            elapsed = time.time() - t0

            # --- save ---
            write_result(mk, test, response_text, elapsed)
            progress[rk] = {
                "time": elapsed,
                "timestamp": datetime.now().isoformat(),
                "chars": len(response_text),
            }
            save_progress(progress)

            status = "✅" if not response_text.startswith("[ERROR") else "❌"
            print(f" {status} {elapsed:.1f}s")

            # gentle delay to avoid rate limits
            time.sleep(2)

    print(f"\n🏁 Done! All {total} runs completed.")
    print(f"   Results in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    run_all()
