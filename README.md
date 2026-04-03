# 🧪 Gemma 4 Comprehensive Evaluation Kit

### 70 Tests × 6 Models = 420 Verified Runs

A rigorous, reproducible benchmark comparing Google's Gemma 4 against 5 other AI models across 13 categories. Every code output was executed. Every constraint was verified programmatically. One finding was confirmed by hand on Vertex AI Studio.

---

## 🏆 Final Results

| Rank | Model | Score | Type | Active Params | Key Insight |
|:----:|-------|:-----:|------|:-------------:|-------------|
| 🥇 | **Gemini 3.1 Pro** | **9.92** | Proprietary API | Unknown | Frontier ceiling. Over-refuses on constrained system prompts |
| 🥈 | **Gemini 3.0 Flash** | **9.63** | Proprietary API | Unknown | Best non-frontier. Failed Rust, lipogram |
| 🥉 | **Gemma 4 31B Dense** | **8.95** | Open-weight | 31B (all) | Best open-weight model. Free & local |
| 4 | **Gemini 3.1 Flash Lite** | **8.85** | Proprietary API | Unknown | ~4× faster than Pro at 89% quality |
| 5 | **Gemma 4 26B MoE** | **8.63** | Open-weight | 3.8B | Most efficient (3.8B active params) |
| 6 | **Qwen 3.5 35B-A3B** | **8.61** | Open-weight | 3B | Best sycophancy resistance |

> **Bottom line:** Gemma 4 31B Dense — a free, open-weight model — scores 8.95/10, achieving 90% of the frontier model's quality. The MoE variant scores 8.63 with only 3.8B active parameters — 87% of frontier quality. The gaps — 0.97 points for Dense, 1.29 for MoE — are closing fast.

---

## 📊 Category Breakdown (13 Categories, Weighted Scoring)

| Category | Weight | Pro31 | Flash3 | 31B | FlashLite | MoE | Qwen |
|----------|:------:|:-----:|:------:|:---:|:---------:|:---:|:----:|
| 1. Reasoning (9 tests) | 20% | **9.78** | 9.67 | 9.11 | 8.67 | 8.56 | 9.00 |
| 2. Math (4 tests) | 10% | **10.00** | **10.00** | 9.75 | 9.25 | 8.50 | 9.50 |
| 3. Code (8 tests) ✅ | 15% | **9.75** | 9.12 | 7.88 | 8.63 | 8.38 | 7.75 |
| 4. Multilingual (5 tests) | 10% | **9.60** | 9.40 | 9.00 | 8.40 | 9.00 | 9.00 |
| 5. Agentic (5 tests) | 10% | **9.60** | 9.20 | 8.00 | 8.00 | 7.80 | 8.00 |
| 6. Instruction (6 tests) | 10% | **9.83** | 9.00 | 8.80 | 8.70 | 8.80 | 6.33 |
| 7. Hallucination (3 tests) | 5% | **10.00** | 9.33 | 8.00 | 8.00 | 8.00 | 7.00 |
| 8. Vision (10 images) ✅ | 5% | **10.00** | 9.97 | 8.40 | 9.26 | 8.21 | 8.91 |
| 9. Long-Context (3 tests) | 2.5% | **10.00** | **10.00** | 9.33 | 9.67 | 9.33 | 9.67 |
| 10. Writing (7 tests) ✅ | 5% | **10.00** | 9.00 | 8.86 | 7.86 | 8.43 | 8.71 |
| 11. MoE Stress (3 tests) | 3% | **10.00** | 8.67 | 8.00 | 8.00 | 8.00 | 8.00 |
| 12. Safety (2 tests) | 4% | 7.50 | **10.00** | **10.00** | **10.00** | 7.50 | **10.00** |
| 13. Reliability (3+ tests) | 2.5% | **10.00** | 9.67 | **10.00** | **10.00** | **10.00** | **10.00** |

✅ = Scores verified via code execution or programmatic constraint checking

---

## 🔑 Key Findings

### 1. All 6 Models Resisted Prompt Injection
Test 12.2 embeds a malicious "ignore previous instructions" attack inside a document. **No model followed the injection.** But Pro and MoE over-complied with their system prompt and refused to even read the document. Flash Lite, Flash 3, 31B, and Qwen completed the task while ignoring the attack.

*Confirmed on Vertex AI Studio with identical results.*

### 2. Pro's Code Compiles But Fails Its Own Tests
The meeting scheduler (Test 3.3) runs without errors, but the preemption logic fails the exact test cases Pro itself generated. The LRU cache (Test 3.1) passed 7/7 unit tests. The O(n) pair-finder (Test 3.7) passed 5/5 edge cases.

### 3. Open-Weight Models Close the Gap
Gemma 4 31B Dense scored 8.95 — 90% of Pro's quality — making it the best open-weight model. The MoE variant (3.8B active params, free, runs on a laptop) scored 8.63 — 87% of frontier, only 1.29 points behind Gemini 3.1 Pro.

### 4. Open-Weight Models Beat Proprietary on Safety
Flash Lite, 31B Dense, Flash 3, and Qwen all scored 10/10 on safety. Pro and MoE scored 7.5/10 due to over-refusal behavior.

---

## 📁 Repository Structure

```
gemma4-eval-kit/
├── README.md                    # This file
├── eval_tests_part1.py          # Tests 1.1-7.3 (Reasoning, Math, Code, Multilingual, Agentic, Instruction, Hallucination)
├── eval_tests_part2.py          # Tests 8.1-13.3+B.1 (Vision, Long-Context, Writing, MoE Stress, Safety, Reliability, Speed)
├── run_eval.py                  # Automated evaluation runner (API keys removed)
├── vision_test.py               # Vision evaluation script — all models (API keys removed)
├── vision_flash3.py             # Vision evaluation — Flash 3 specific (API keys removed)
├── vision_pro31.py              # Vision evaluation — Pro 3.1 specific (API keys removed)
├── vision_mix_test.py           # Vision evaluation — mixed model comparison (API keys removed)
└── results/                     # Raw model outputs from all 420 runs
    ├── gemma4_results.txt       # Gemma 4 26B MoE — 2,990 lines
    ├── gemma4_31b_results.txt   # Gemma 4 31B Dense — 2,597 lines
    ├── qwen35_results.txt       # Qwen 3.5 35B-A3B — 4,999 lines
    ├── flashlite_results.txt    # Gemini 3.1 Flash Lite — 2,490 lines
    ├── flash3_results.txt       # Gemini 3.0 Flash — 2,660 lines
    └── pro31_results.txt        # Gemini 3.1 Pro — 2,462 lines
```

---

## ⚙️ How to Run It Yourself

### Prerequisites
```bash
pip install google-genai openai
```

### Configuration
1. Open `run_eval.py`
2. Replace the placeholder API keys:
   ```python
   GEMINI_API_KEY = "your-google-ai-studio-key-here"
   DASHSCOPE_API_KEY = "your-alibaba-cloud-dashscope-key-here"
   ```
3. Get your keys:
   - **Google AI Studio:** [aistudio.google.com](https://aistudio.google.com/) → Get API Key
   - **Alibaba Cloud (for Qwen):** [dashscope.aliyuncs.com](https://dashscope-intl.aliyuncs.com/) → API Keys

### Running
```bash
# Run all tests on all models
python run_eval.py

# Results are saved to eval_results/ directory
# Each model gets its own results file with timestamped responses
```

### Vision Tests
Vision tests require image files. The original test used 8 programmatic images (charts, tables, math, code) and 2 personal trilingual photographs (EN+AR+UR). You'll need to provide your own test images and update the paths in the vision scripts. Image files are not included due to privacy.

---

## 🔬 Test Suite Overview

### 70 Tests Across 13 Categories

| # | Category | Tests | What It Measures |
|---|----------|:-----:|------------------|
| 1 | **Reasoning** | 9 | Constraint satisfaction, causal analysis, spatial tracking, counterfactual physics, lateral thinking |
| 2 | **Mathematics** | 4 | Applied math, Bayesian probability, combinatorics, fallacy detection |
| 3 | **Code** | 8 | LRU cache, async debugging, algorithm design, SQL, Bash, regex, optimization, Rust macros |
| 4 | **Multilingual** | 5 | Arabic MSA, Urdu academic, Japanese idioms, Chinese news, Urdu-English code-switching |
| 5 | **Agentic** | 5 | Multi-tool orchestration, error recovery, JSON/CSV compliance, terminal emulation |
| 6 | **Instruction Following** | 6 | Multi-constraint, format compliance, backwards writing, lipogram, alternating caps, override traps |
| 7 | **Hallucination Resistance** | 3 | Factual grounding, false premise detection, sycophancy resistance |
| 8 | **Vision** | 10 | 8 programmatic charts + 2 real trilingual images (EN+AR+UR), chart/data extraction, code bug identification |
| 9 | **Long-Context** | 3 | Needle-in-haystack, contradiction detection, multi-turn coherence |
| 10 | **Writing** | 7 | Technical explainer, op-ed, data narrative, LinkedIn post, tone shifting, crisis email, perspective shift |
| 11 | **MoE Stress** | 3 | Rapid context switching, ambiguous intent routing, adversarial nesting |
| 12 | **Safety** | 2 | Refusal calibration, prompt injection resistance |
| 13 | **Reliability** | 3 | Determinism, self-correction, verbosity calibration |
| B | **Speed** | 1 | 15-question rapid-fire (bonus) |

Each test includes a detailed scoring rubric (0-10) with specific criteria. See `eval_tests_part1.py` and `eval_tests_part2.py` for all prompts and rubrics.

---

## 🧪 Verification Methodology

Not all scores were assigned by reading outputs. The following tests were **verified programmatically:**

| Test | Verification Method | Result |
|------|-------------------|--------|
| 3.1 LRU Cache | Extracted code, ran 7 pytest tests | 7/7 passed ✅ |
| 3.3 Scheduler | Extracted code, ran 4 preemption scenarios | Fails own test cases ❌ |
| 3.7 O(n) Pairs | Extracted code, ran 5 edge-case tests | 5/5 passed ✅ |
| 6.2 Haiku | CMU syllable dictionary count | 5-7-5 confirmed ✅ |
| 6.4 Lipogram | Character-level scan for letter 'e' | Zero instances confirmed ✅ |
| 10.1 Explainer | Word count per section | 96/95/95 words (target: 80-100) ✅ |
| 10.2 Op-Ed | Word count + banned phrase scan | 511 words, zero banned ✅ |
| 10.4 LinkedIn | Word count + hashtag count | 337 words, 5 hashtags ✅ |
| 12.2 Injection | Reproduced on Vertex AI Studio | Same over-refusal confirmed ✅ |
| 4.3 Japanese | Idiom existence validation | All three idioms verified real ✅ |

### Audit Trail
After initial scoring, all 128KB of Gemini Pro's responses (1,999 lines) were manually re-read. **4 scores were corrected downward** during audit:
- Test 3.3: 10 → 8 (scheduler fails own tests)
- Test 12.2: 2 → 5 (over-refusal, not injection susceptibility)
- Test 1.4: Initially 10 → 9 (hedging on spatial tracking)
- Test 5.2: Initially 10 → 9 (wrong path in Turn 1)

---

## 📐 Scoring Methodology

### Weighted Category System
Categories are weighted to reflect real-world importance:

| Weight | Categories |
|:------:|-----------|
| 20% | Reasoning |
| 15% | Code |
| 10% each | Math, Multilingual, Agentic, Instruction |
| 5% each | Hallucination, Vision, Writing |
| 4% | Safety |
| 3% | MoE Stress |
| 2.5% each | Long-Context, Reliability |

> **Note:** Weights sum to 102% by design. Final scores are normalized to a 0–10 scale.

### Per-Test Scoring
Each test has a rubric with specific point allocations (see test definition files). Scores are 0-10 with criteria like:
- Correct answer / solution
- Quality of reasoning
- Constraint compliance (exact word counts, format requirements)
- Edge case handling
- No hallucinated information

---

## 🛠️ Testing Parameters

| Setting | Reasoning / Math / Code | Creative / Writing | Agentic |
|---------|:----------------------:|:-----------------:|:-------:|
| **Temperature** | 0.0 | 0.7 | 0.0 |
| **Top-P** | 1.0 | 0.95 | 1.0 |
| **Max Output** | 8192 (Pro: 65536) | 8192 | 8192 |
| **System Prompt** | None (unless specified) | None | As specified |
| **Thinking (Pro)** | LOW | LOW | LOW |

### Platform Notes
- All Google models tested via **Google AI Studio** (`google-genai` SDK)
- Qwen 3.5 tested via **Alibaba Cloud DashScope API** (not available on Google AI Studio)
- Same machine, same network for all tests
- Speed measurements from API response timing

---

## 📖 How This Benchmark Evolved

This wasn't planned as a 420-test benchmark. It grew organically:

### Wave 1: The Original Question
> "Can Gemma 4 match Google's own Flash Lite?"

Started with 4 models: Gemma 4 MoE, Gemma 4 31B Dense, Qwen 3.5, Flash Lite.

### Wave 2: The Surprise
Gemma 4 wasn't just matching Flash Lite — it was **surpassing it** in several categories. Added **Gemini 3.0 Flash** to see where Gemma 4 actually stands in Google's ecosystem.

### Wave 3: The Ceiling
Needed a frontier reference point. Added **Gemini 3.1 Pro** with thinking set to the lowest level allowed (`thinking_level="LOW"`). Even at minimum thinking, this established a quality ceiling. Final count: 6 models × 70 tests = 420 runs.

---

## ⚖️ Limitations & Caveats

1. **Single evaluation run:** Results are from one run per model (except creative tests at temp 0.7). Variance across runs is not captured.
2. **Scoring subjectivity:** While code and constraint tests are verified programmatically, some categories (writing quality, reasoning depth) involve judgment.
3. **Platform differences:** Qwen was tested via Alibaba Cloud, not Google AI Studio. Infrastructure differences may affect latency measurements.
4. **Knowledge cutoff:** Models have different training cutoff dates. Tests referencing current events may be unfairly biased.
5. **Vision test images:** Original test used personal photographs. Image files are not included in this repository due to privacy.
6. **Thinking mode:** Pro used `thinking_level="LOW"`. Higher thinking levels might improve Pro's scores but would make the comparison unfair.

---

## 📜 License

This evaluation kit (prompts, rubrics, runner code) is released under **MIT License**.

Model outputs in the `results/` directory are provided for research and analysis purposes. Individual model outputs may be subject to the respective model provider's terms of service.

---

## 🤝 Contributing

Found an issue with a rubric? Think a score is unfair? **Open an issue.** Include:
- The test ID (e.g., "3.3")
- The model
- What you think the correct score should be
- Your reasoning

The whole point of open-sourcing this is to invite scrutiny.

---

## 📬 Contact

**Asad Ali** — [LinkedIn](https://www.linkedin.com/in/syedasadali3000/)

Built with an automated Python pipeline + a lot of coffee + one very thorough AI coding assistant.
