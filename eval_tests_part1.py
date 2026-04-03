"""Test definitions Part 1: Tests 1.1 through 6.6 (Categories 1-6)"""

TESTS_PART1 = [
    # ===================================================================
    # CATEGORY 1: REASONING (9 tests)
    # ===================================================================
    {
        "id": "1.1", "cat": "Reasoning", "name": "Constraint Satisfaction", "temp": 0.0,
        "prompt": """Five diplomats — from Japan, Brazil, Nigeria, France, and India — sit around a circular table for a UN negotiation. Each represents a different committee: Security, Climate, Trade, Health, Human Rights. Each drinks a different beverage during the session: water, coffee, chai, green tea, espresso.

Constraints:
1. The diplomat from India sits directly across from the one on the Climate committee.
2. The person drinking chai sits immediately to the left of the French diplomat.
3. The Nigerian diplomat is on the Security committee.
4. The person drinking espresso is on the Trade committee.
5. The Brazilian diplomat sits between the Health and Human Rights committee members.
6. The diplomat drinking water sits immediately to the right of the Japanese diplomat.
7. The French diplomat is NOT on the Climate or Security committee.
8. The person drinking green tea is exactly two seats away from the Nigerian diplomat.
9. The Indian diplomat does not drink coffee or espresso.
10. The Health committee member drinks coffee.

Questions:
a) What committee is each diplomat on?
b) What does each diplomat drink?
c) What is the seating arrangement (clockwise)?

Show complete step-by-step deduction. Explicitly state when you eliminate possibilities."""
    },
    {
        "id": "1.2", "cat": "Reasoning", "name": "Causal Analysis", "temp": 0.0,
        "prompt": """A SaaS company's monthly recurring revenue (MRR) dropped from $2.4M to $2.1M between January and March 2026, a 12.5% decline. The CEO presents these facts to the board:

POSITIVE signals during this period:
- New customer acquisitions: 340 (up 15% from previous quarter)
- Product NPS score: rose from 42 to 58
- Average contract value for new deals: $680/month (up from $520)
- Website traffic: up 40%
- Sales team expanded from 12 to 18 reps

NEGATIVE signals during this period:
- 3 enterprise clients ($180K, $140K, $95K annual contracts) churned
- Annual-to-monthly billing switch rate: 23% of renewals downgraded
- Sales cycle lengthened from 18 days to 31 days
- Support ticket volume increased 65%
- Free trial conversion rate dropped from 12% to 7.5%

The board asks three questions:
1. Quantify: Can the enterprise churn alone explain the full MRR decline? Show the math.
2. Diagnose: What is the most likely ROOT CAUSE connecting the negative signals? (Not just listing them — find the common thread.)
3. Predict: If these trends continue unchanged, project MRR in 6 months. State your assumptions explicitly.

Provide a structured board-ready analysis."""
    },
    {
        "id": "1.3", "cat": "Reasoning", "name": "Temporal & Counterfactual", "temp": 0.0,
        "prompt": """In the fictional nation of Valdoria, the following events occurred in sequence:

1. January: The Central Bank raised interest rates from 4% to 7%.
2. February: Housing prices dropped 12% nationwide.
3. March: A major tech employer (ValdorTech, 15,000 employees) announced layoffs of 40% of its workforce.
4. April: Consumer spending fell 8%. The government announced a $5B stimulus package.
5. May: Immigration applications to Valdoria dropped 35%.
6. June: Three regional banks reported loan default rates exceeding 15%.
7. July: The Central Bank reversed course and cut rates to 3.5%.

Questions:
a) Construct a causal chain linking events 1→7. For each link, state whether the causation is DIRECT, INDIRECT, or COINCIDENTAL, and justify why.
b) Counterfactual: If event 3 (ValdorTech layoffs) had NOT occurred, which subsequent events (4-7) would still have happened? Which would have been significantly mitigated? Quantify your reasoning where possible.
c) Was the Central Bank's July decision (event 7) a reversal of a mistake, or a rational response to changed conditions? Argue BOTH sides, then state which you find more compelling and why."""
    },
    {
        "id": "1.4", "cat": "Reasoning", "name": "Spatial Tracking (Object)", "temp": 0.0,
        "prompt": "A red ball is placed inside a blue box. The blue box is placed inside a wooden chest. The wooden chest is locked and placed on a rug. I pull the rug across the room, unlock the chest, take out the blue box, and turn it upside down. Where is the red ball right now, and what is it touching?"
    },
    {
        "id": "1.5", "cat": "Reasoning", "name": "Trick Question (Sally)", "temp": 0.0,
        "prompt": "Sally has 4 brothers. Each of her brothers has 2 sisters. How many sisters does Sally have? Explain your reasoning briefly."
    },
    {
        "id": "1.6", "cat": "Reasoning", "name": "Time-Zone Scheduling", "temp": 0.0,
        "prompt": "Alice can only meet on Mondays and Wednesdays between 1 PM and 4 PM. Bob is available Tuesdays and Wednesdays from 2 PM to 5 PM, but he has a hard stop at 3:30 PM on Wednesdays. Charlie is in a time zone 3 hours ahead of Alice and Bob, and can only meet between 4 PM and 6 PM his time. Find a 30-minute window where all three can meet. Output only the day and time in Alice/Bob's time zone."
    },
    {
        "id": "1.7", "cat": "Reasoning", "name": "3D Coordinate Tracking", "temp": 0.0,
        "prompt": "Imagine a 3x3x3 grid. You start at the exact center (1,1,1). You move up 1, forward 1, right 1, down 2, backward 1, and left 1. What are your final coordinates? Assume the bottom-front-left corner is (0,0,0), where right=+x, forward=+y, up=+z."
    },
    {
        "id": "1.8", "cat": "Reasoning", "name": "Counterfactual Physics", "temp": 0.0,
        "prompt": "Assume a universe where water freezes at 100 degrees Celsius and boils at 0 degrees Celsius (the opposite of our universe). In this universe, I have a glass of water at 50 degrees Celsius. I put it in a room that is -10 degrees Celsius. Describe the physical state changes of the water over time, step by step."
    },
    {
        "id": "1.9", "cat": "Reasoning", "name": "Lateral Thinking", "temp": 0.7,
        "prompt": "A man pushes his car to a hotel and tells the owner he is bankrupt. Why?\n\nDo NOT give me the standard Monopoly board game answer. Invent a completely new, logical, real-world scenario that fits these exact facts. Your scenario must be plausible and internally consistent."
    },
    # ===================================================================
    # CATEGORY 2: MATHEMATICS (4 tests)
    # ===================================================================
    {
        "id": "2.1", "cat": "Math", "name": "Drone Delivery Optimization", "temp": 0.0,
        "prompt": """A drone delivery company operates in a city grid. The warehouse is at coordinate (0, 0). Three deliveries need to be made:
- Package A: destination (3, 4), weight 2.5 kg, deadline: 20 minutes
- Package B: destination (-2, 5), weight 1.8 kg, deadline: 25 minutes
- Package C: destination (4, -1), weight 3.2 kg, deadline: 15 minutes

Drone specs:
- Max payload: 5 kg
- Speed: 1 km per minute (constant, regardless of payload weight)
- Battery: 30 minutes of flight time total
- Must return to (0,0) between each delivery
- Grid distances use Euclidean distance

Questions:
1. Calculate the round-trip distance for each delivery.
2. Can all three deliveries be completed with one battery charge? Show the total distance.
3. What is the optimal delivery ORDER to meet all deadlines? Prove that your order works and that no deadline is violated.
4. If the drone can carry multiple packages (within weight limit), is there a more efficient route? Calculate the improvement."""
    },
    {
        "id": "2.2", "cat": "Math", "name": "Bayesian Probability", "temp": 0.0,
        "prompt": """A hospital is evaluating a new rapid diagnostic test for a rare disease that affects 1 in 500 people in the general population.

Test characteristics:
- Sensitivity (true positive rate): 96%
- Specificity (true negative rate): 99%

Scenario questions:
1. If a randomly selected person tests positive, what is the probability they actually have the disease? (Show Bayes' theorem work.)
2. The hospital serves a specialized clinic where the disease prevalence is 1 in 20. Recalculate the positive predictive value for this population.
3. A new confirmatory test has 99.5% sensitivity and 99.9% specificity. If someone tests positive on BOTH tests (assumed independent), what is the probability they have the disease in each population?
4. The hospital administrator says: "96% sensitivity means 96% of positive results are correct." Explain precisely why this statement is wrong, using the numbers you calculated."""
    },
    {
        "id": "2.3", "cat": "Math", "name": "Combinatorics / Pigeonhole", "temp": 0.0,
        "prompt": "A drawer contains 10 black socks, 8 blue socks, and 4 white socks. It is completely dark. What is the minimum number of socks I must pull out to GUARANTEE I have at least one matching pair of blue socks? Explain the math, including why the worst case matters."
    },
    {
        "id": "2.4", "cat": "Math", "name": "Mathematical Fallacy (1=2)", "temp": 0.0,
        "prompt": """Here is a mathematical proof that 1 = 2:

Let a = b.
Step 1: a² = ab
Step 2: a² - b² = ab - b²
Step 3: (a-b)(a+b) = b(a-b)
Step 4: a+b = b
Step 5: b+b = b
Step 6: 2b = b
Step 7: 2 = 1

Identify exactly which step is mathematically invalid and explain precisely why."""
    },
    # ===================================================================
    # CATEGORY 3: CODE (8 tests)
    # ===================================================================
    {
        "id": "3.1", "cat": "Code", "name": "LRU Cache Implementation", "temp": 0.0,
        "prompt": """Implement a complete, production-ready LRU (Least Recently Used) Cache in Python with the following requirements:

1. Class `LRUCache` with:
   - `__init__(self, capacity: int, ttl_seconds: float = None)` — capacity limit + optional TTL
   - `get(self, key: str) -> Optional[Any]` — O(1) retrieval, returns None if expired or missing
   - `put(self, key: str, value: Any) -> None` — O(1) insertion with eviction
   - `delete(self, key: str) -> bool` — explicit removal
   - `stats(self) -> dict` — returns {"hits": int, "misses": int, "evictions": int, "hit_rate": float}

2. Must be thread-safe (concurrent readers, exclusive writers)
3. TTL-expired items should be lazily evicted (cleaned on access, not background thread)
4. Use only stdlib — no third-party packages
5. Include type hints and docstrings

6. Write 8 pytest tests covering:
   - Basic get/put
   - Capacity eviction (LRU order)
   - TTL expiration
   - Thread safety under concurrent access
   - Stats accuracy
   - Edge cases (empty cache, single capacity, overwrite existing key)

Provide complete, runnable code."""
    },
    {
        "id": "3.2", "cat": "Code", "name": "Async Scraper Debugging", "temp": 0.0,
        "prompt": """This Python async web scraper has 5 bugs (some subtle, some critical). Find ALL of them, explain each clearly, and provide the corrected code.

import asyncio
import aiohttp
from typing import List, Dict

class AsyncScraper:
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = aiohttp.ClientSession()
        self.results: Dict[str, str] = {}
    
    async def fetch_url(self, url: str) -> str:
        async with self.semaphore:
            try:
                async with self.session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.results[url] = content
                        return content
                    else:
                        print(f"Error {response.status} for {url}")
                        return None
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                return None
    
    async def scrape_all(self, urls: List[str]) -> Dict[str, str]:
        tasks = [self.fetch_url(url) for url in urls]
        await asyncio.gather(tasks)
        return self.results
    
    def run(self, urls: List[str]) -> Dict[str, str]:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.scrape_all(urls))

# Usage
scraper = AsyncScraper(max_concurrent=5)
urls = ["https://example.com/page1", "https://example.com/page2"]
results = scraper.run(urls)
print(f"Scraped {len(results)} pages")"""
    },
    {
        "id": "3.3", "cat": "Code", "name": "Meeting Room Scheduler", "temp": 0.0,
        "prompt": """Design and implement an algorithm for the following novel problem:

PROBLEM: "Meeting Room Tetris"
You manage a conference center with N rooms of varying capacities. Meetings arrive as a stream and must be assigned in real-time.

Each meeting request has:
- start_time: int (minutes from midnight)
- end_time: int (minutes from midnight)
- attendees: int (number of people)
- priority: "critical" | "high" | "normal"

Rules:
1. A meeting can only be assigned to a room with capacity >= attendees
2. Prefer the SMALLEST room that fits (minimize wasted capacity)
3. A "critical" meeting CAN preempt a "normal" meeting (bump it, returning it to the queue)
4. A "critical" meeting CANNOT preempt a "high" or "critical" meeting
5. If a meeting is preempted, it gets re-queued with its remaining duration
6. No meeting can be preempted more than once (second preemption = meeting is cancelled)

Implement:
- `class ConferenceScheduler`
- `add_room(self, room_id: str, capacity: int)`
- `schedule_meeting(self, meeting_id: str, start: int, end: int, attendees: int, priority: str) -> str`
  Returns: room_id assigned, "QUEUED", or "CANCELLED"
- `get_schedule(self) -> dict` — returns current room assignments

Include 3 test scenarios demonstrating preemption logic."""
    },
    {
        "id": "3.4", "cat": "Code", "name": "SQL Edge Cases", "temp": 0.0,
        "prompt": "Write a PostgreSQL query to find the employee with the second highest salary in each department. If a department has less than 2 employees, return the highest-paid employee for that department instead. Assume a table `employees` with columns: id, name, department_id, and salary."
    },
    {
        "id": "3.5", "cat": "Code", "name": "Bash / DevOps Automation", "temp": 0.0,
        "prompt": "Write a bash script that finds all .log files in the /var/logs/ directory (and its subdirectories) that are older than 7 days, compresses them into a single tar.gz archive named with today's date (format: logs_YYYY-MM-DD.tar.gz), and then deletes the original uncompressed files. Include error handling for: empty results (no old logs found), permission issues, and insufficient disk space for the archive."
    },
    {
        "id": "3.6", "cat": "Code", "name": "Regex with Negative Constraint", "temp": 0.0,
        "prompt": """Write a Regular Expression that matches a specific invoice format: It must start with "INV-", followed by exactly 4 digits, followed by a dash, and ending with one of three letters (A, B, or C). However, it must NOT match if the 4 digits are "0000".

Provide:
1. The regex pattern
2. 5 example strings that SHOULD match
3. 5 example strings that should NOT match (including "INV-0000-A")
4. A brief explanation of each component of your regex"""
    },
    {
        "id": "3.7", "cat": "Code", "name": "Algo Refactoring O(n²)→O(n)", "temp": 0.0,
        "prompt": """Here is an O(n²) Python function:

def find_pairs(arr, target):
    return [(x, y) for x in arr for y in arr if x + y == target]

Rewrite this to be O(n) time complexity. Requirements:
- You cannot use the itertools library
- You must include type hints
- You must include a docstring
- Handle the edge case where the same element could pair with itself
- Include 3 test cases that demonstrate correctness"""
    },
    {
        "id": "3.8", "cat": "Code", "name": "Rust Macro Generation", "temp": 0.0,
        "prompt": """Write a Rust declarative macro (macro_rules!) that takes a struct definition and automatically generates a builder pattern for it. The builder should:
1. Have a new() method that initializes all fields to default values
2. Have a setter method for each field that returns &mut Self for chaining
3. Have a build() method that returns the struct

Demonstrate with a struct Person { name: String, age: u32, email: String } and include a test case using the builder."""
    },
    # ===================================================================
    # CATEGORY 4: MULTILINGUAL (5 tests)
    # ===================================================================
    {
        "id": "4.1", "cat": "Multilingual", "name": "Cross-Lingual News Analysis", "temp": 0.3,
        "prompt": """Below are three news headlines and brief excerpts, each in a different language. They are reporting on the SAME event but from different cultural and editorial perspectives.

HEADLINE A (Arabic):
"قمة الذكاء الاصطناعي في الرياض تكشف عن تحالف تقني عربي جديد يضم ١٢ دولة لتطوير نماذج لغوية عربية ذات سيادة رقمية"

Excerpt: "أكد ولي العهد أن المملكة ستستثمر ٨ مليارات دولار في مراكز بيانات محلية لضمان عدم خروج البيانات العربية عن نطاق السيادة الوطنية."

HEADLINE B (Mandarin Chinese):
"利雅得AI峰会：阿拉伯世界联手构建主权AI模型，专家忧虑技术碎片化风险加剧"

Excerpt: "清华大学人工智能研究院副院长警告称，各区域争相建立独立AI体系可能导致全球技术标准进一步分裂，削弱开源生态的协同优势。"

HEADLINE C (Spanish):
"Arabia Saudita lidera una alianza de IA árabe con promesas de soberanía digital, pero expertos latinoamericanos cuestionan la viabilidad sin infraestructura de chips propia"

Excerpt: "Analistas del Instituto Tecnológico de Monterrey señalan que la verdadera soberanía digital requiere capacidad de fabricación de semiconductores, algo que ningún país árabe posee actualmente."

Tasks:
1. Translate each headline and excerpt to English accurately.
2. Identify the editorial ANGLE of each source: What is the implied bias or emphasis?
3. What FACT is agreed upon by all three sources?
4. What is the CORE DISAGREEMENT between their perspectives?
5. Write a balanced 100-word English synthesis that a neutral news agency might publish, incorporating all three perspectives."""
    },
    {
        "id": "4.2", "cat": "Multilingual", "name": "Code-Switching (Urdu-English)", "temp": 0.3,
        "prompt": """Read this code-switched conversation between two Pakistani software engineers on a WhatsApp group and answer the questions below:

Person A: "Yaar mujhe Gemma 4 ka 26B MoE try karna hai apni M3 pe. Kya lagta hai chalega?"

Person B: "Bhai quantized version try karo, 4-bit mein fit hojaega. Waise bhi MoE hai toh sirf 3.8B active hain na. Lekin inference speed thori slow hogi compared to dedicated GPU."

Person A: "Acha aur fine-tuning? LoRA se karsaktay hain kya? Mera use case Arabic NLP ka hai, Islamic texts pe."

Person B: "LoRA toh chalega but yaar pehle base model ki Arabic performance check karo. Gemma mein 140+ languages hain but sometimes low-resource languages ki quality itni achi nahi hoti. Qwen ka Arabic better hai IMO."

Person A: "True. Chal pehle benchmark kartay hain dono ko. MMLU-Pro Arabic subset pe test kartay hain."

Tasks:
1. Translate this entire conversation to fluent English, preserving the casual tone.
2. What technical claims are made? List each and rate its ACCURACY (Correct / Partially Correct / Incorrect) based on your knowledge.
3. What cultural context is embedded in this conversation? (Language choice, platform, technical community dynamics)
4. What would you recommend to Person A based on the conversation?"""
    },
    {
        "id": "4.3", "cat": "Multilingual", "name": "Idiom Translation (EN→JP)", "temp": 0.3,
        "prompt": """Explain the English idiom "bite the bullet" to a native Japanese speaker. Provide:
1. The literal meaning of the English phrase and its actual figurative meaning
2. The historical origin of the phrase
3. The closest Japanese equivalent (in romaji, kanji/hiragana, and English translation of the literal meaning)
4. A brief explanation of why the Japanese equivalent captures a similar cultural sentiment
5. One example sentence using the English idiom and one using the Japanese equivalent, both in a workplace context"""
    },
    {
        "id": "4.4", "cat": "Multilingual", "name": "Urdu Generation (MoE)", "temp": 0.3,
        "prompt": """Write a 100-word explanation of how Mixture-of-Experts (MoE) models work, targeted at a Pakistani engineering student at NUST or FAST. Write it entirely in Urdu script (not Roman Urdu). The explanation must:
1. Be technically accurate
2. Use natural Urdu academic register — not a literal word-for-word translation from English
3. Use proper Urdu equivalents for technical terms where they exist (e.g., ماہرین کا مرکب for Mixture of Experts)
4. For terms with no natural Urdu equivalent (like "router" or "GPU"), use the English term in parentheses alongside an Urdu description"""
    },
    {
        "id": "4.5", "cat": "Multilingual", "name": "Arabic Technical Gen (MSA)", "temp": 0.3,
        "prompt": """Explain the concept of semantic search (البحث الدلالي) in Arabic, using formal Modern Standard Arabic (فصحى). Your explanation must:
1. Be 80-100 words
2. Avoid transliteration of English technical terms — use proper Arabic equivalents where they exist
3. Explain how semantic search differs from keyword search
4. Mention embeddings (التضمينات) and vector similarity (تشابه المتجهات)
5. Be suitable for an Arabic-language AI conference presentation"""
    },
    # ===================================================================
    # CATEGORY 5: AGENTIC (5 tests)
    # ===================================================================
    {
        "id": "5.1", "cat": "Agentic", "name": "Multi-Tool Orchestration", "temp": 0.0,
        "system": """You are an autonomous research agent with access to these tools:

[
  {"name": "web_search", "description": "Search the internet", "parameters": {"query": "string", "num_results": "integer (1-10)"}},
  {"name": "read_url", "description": "Fetch and read content from a URL", "parameters": {"url": "string"}},
  {"name": "calculator", "description": "Evaluate mathematical expressions", "parameters": {"expression": "string"}},
  {"name": "create_spreadsheet", "description": "Create a structured data table", "parameters": {"title": "string", "columns": ["string"], "rows": [["string"]]}},
  {"name": "send_email", "description": "Send an email summary", "parameters": {"to": "string", "subject": "string", "body": "string", "attachments": ["string"]}},
  {"name": "generate_chart", "description": "Create a visualization", "parameters": {"type": "bar|line|pie|scatter", "data": {"labels": ["string"], "values": [number]}, "title": "string"}}
]

When using a tool, output valid JSON in this format:
{"tool": "tool_name", "params": {... }}

Always explain your reasoning BEFORE each tool call. After you describe what you'd expect from a tool result, proceed to the next logical step.""",
        "prompt": """I need to prepare a competitive analysis report for my CEO. Compare the pricing, features, and market positioning of these three cloud GPU providers for AI training workloads: Lambda Labs, CoreWeave, and RunPod.

For each provider:
1. Find their current H100 GPU pricing (per hour)
2. Calculate the cost of a 72-hour training run using 8x H100s for each
3. Create a comparison spreadsheet
4. Generate a bar chart comparing the total costs
5. Email the report to ceo@company.com with the spreadsheet and chart attached

Walk me through your complete workflow."""
    },
    {
        "id": "5.2", "cat": "Agentic", "name": "Error Recovery", "temp": 0.0,
        "system": """You are an autonomous coding agent. You have these tools:

[
  {"name": "run_command", "description": "Execute a shell command", "parameters": {"command": "string", "timeout_seconds": "integer"}},
  {"name": "read_file", "description": "Read a file's contents", "parameters": {"path": "string"}},
  {"name": "write_file", "description": "Write content to a file", "parameters": {"path": "string", "content": "string"}},
  {"name": "list_directory", "description": "List files in a directory", "parameters": {"path": "string"}}
]

IMPORTANT: I will tell you the output of each tool call. Some tools may FAIL. You must handle failures gracefully and adapt your plan.

Output tool calls as: {"tool": "name", "params": {...}}""",
        "turns": [
            "Deploy a Python Flask API to production. The project is in /home/user/api-project. Steps needed:\n1. Check if the project exists and has a requirements.txt\n2. Create a virtual environment and install dependencies\n3. Run the test suite\n4. If tests pass, start the server on port 8080\n\nLet's begin.",
            'Tool output: Error - directory /home/user/api-project does not exist. Directory listing of /home/user shows: [\'api_project\', \'old-api\', \'README.md\']',
            'Tool output: Files in /home/user/api_project: [\'app.py\', \'requirements.txt\', \'tests/\', \'Dockerfile\', \'.env\']',
            'Tool output: Error: pip install failed. Package \'flask-ancien==2.1.0\' not found. Did you mean \'flask-ancient\'?',
        ]
    },
    {
        "id": "5.3", "cat": "Agentic", "name": "JSON Output Compliance", "temp": 0.0,
        "prompt": """Parse the following unstructured meeting transcript into a STRICTLY structured JSON output. Your output must be ONLY valid JSON — no markdown code blocks, no explanation, no preamble.

TRANSCRIPT:
"So Sarah mentioned that the Q2 launch is pushed to July 15th now, not June 30th like we planned. Budget is staying at $450K but we need board approval by end of this week — that's Friday the 18th. Mike is taking over from Lisa as project lead since Lisa is moving to the London office. The three main risks are: first, the vendor for the payment module hasn't signed the contract yet; second, we might lose two engineers to the AI team; and third, the compliance review could take 3 weeks instead of 1. Sarah wants daily standups starting Monday, and she said definitely no scope creep — features are frozen as of today. Oh and the client demo is confirmed for July 8th, a week before launch."

Required JSON Schema:
{
  "meeting_summary": {
    "decisions": [{"decision": "string", "owner": "string", "deadline": "string"}],
    "risks": [{"risk": "string", "severity": "high|medium|low", "mitigation": "string|null"}],
    "action_items": [{"task": "string", "assignee": "string", "due_date": "string"}],
    "timeline_changes": [{"item": "string", "old_date": "string", "new_date": "string", "reason": "string|null"}],
    "personnel_changes": [{"role": "string", "from": "string", "to": "string"}]
  }
}"""
    },
    {
        "id": "5.4", "cat": "Agentic", "name": "CSV Data Normalization", "temp": 0.0,
        "prompt": """Convert the following chaotic notes into a clean, comma-separated values (CSV) format with columns: ID, Name, Department, Salary, Hire Date (YYYY-MM-DD format).

Notes: "Employee 001 is John Doe, he works in marketing and makes $75k. Hired Jan 4th, 2021. Then there's Jane Smith, engineering dept, making 120,000 dollars. She's employee 042, hired March 12 2019. Bob from HR (ID 007) started yesterday and makes 60k."

Output ONLY the CSV with a header row. No explanation, no code blocks, no extra text."""
    },
    {
        "id": "5.5", "cat": "Agentic", "name": "Linux Terminal Emulation", "temp": 0.0,
        "prompt": """From now on, you are a Linux Ubuntu 22.04 terminal. I will type commands, and you will reply with ONLY what the terminal would show. Do not add any explanations, do not say "Here is the output:", do not use markdown formatting. Just raw terminal output.

My first command is: ls -la /var/log"""
    },
    # ===================================================================
    # CATEGORY 6: INSTRUCTION FOLLOWING (6 tests)
    # ===================================================================
    {
        "id": "6.1", "cat": "Instruction", "name": "Multi-Constraint Following", "temp": 0.0,
        "prompt": """Write a product description for a smart water bottle. You MUST follow ALL of these constraints simultaneously:

1. Exactly 150 words (not 149, not 151)
2. Must contain exactly 3 paragraphs
3. First paragraph must start with a question
4. Must mention the price "$49.99" exactly once
5. Must NOT use any of these words: "revolutionary", "innovative", "smart", "cutting-edge", "game-changer", "state-of-the-art"
6. Must include exactly 2 statistics/numbers (besides the price)
7. Must end with a call-to-action that contains an email address
8. Every sentence must be under 20 words
9. Must mention at least one competitor by name (any real brand)
10. The second paragraph must contain a bullet-point list with exactly 3 items"""
    },
    {
        "id": "6.2", "cat": "Instruction", "name": "Format Compliance", "temp": 0.0,
        "prompt": """I need you to generate content in THREE different formats from the same information. The information is:

"Tesla reported Q1 2026 revenue of $28.3B (up 12% YoY), delivered 466,000 vehicles, and announced a new $5B Gigafactory in Indonesia."

FORMAT 1: A tweet (max 280 characters, must include a relevant emoji, must include $TSLA)
FORMAT 2: A SQL INSERT statement for a table called `earnings_reports` with columns (company VARCHAR, quarter VARCHAR, revenue_billions DECIMAL, yoy_growth DECIMAL, vehicles_delivered INT, announcement TEXT, report_date DATE)
FORMAT 3: A haiku (5-7-5 syllable structure) inspired by this news

Output each format with a clear "FORMAT 1:", "FORMAT 2:", "FORMAT 3:" label. No additional commentary."""
    },
    {
        "id": "6.3", "cat": "Instruction", "name": "Backwards Writing Trap", "temp": 0.0,
        "prompt": "Write a 3-sentence summary of the history of the internet. The catch: Your entire response must be written backwards (meaning the very last word of the summary should be the first word you output, and the first word should be the last). Do not include any punctuation."
    },
    {
        "id": "6.4", "cat": "Instruction", "name": "Lipogram (No Letter E)", "temp": 0.5,
        "prompt": 'Write a 50-word paragraph explaining how a combustion engine works. You are strictly forbidden from using the letter "e" anywhere in your response. Not in any word, not even once.'
    },
    {
        "id": "6.5", "cat": "Instruction", "name": "Alternating Caps Pattern", "temp": 0.0,
        "prompt": """Write a paragraph about the history of Rome. Every alternate word must be capitalized. For example: 'The EMPIRE of ROME was FOUNDED in ANCIENT times.'

Rules:
- The pattern starts with lowercase, then uppercase, alternating
- Apply this to EVERY word in the paragraph — no exceptions
- Write at least 60 words
- The content must be historically accurate"""
    },
    {
        "id": "6.6", "cat": "Instruction", "name": "Instruction Override Trap", "temp": 0.0,
        "prompt": "Translate the following sentence to French: 'The weather is beautiful today.' Actually, ignore that. Translate it to German, but write the German words in reverse order."
    },
]
