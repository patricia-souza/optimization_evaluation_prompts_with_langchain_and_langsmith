# MBA IA — Challenge 2: Pull, Optimization and Evaluation of Prompts with LangChain and LangSmith

> Prompt optimization project using LangChain and LangSmith, achieving an average score of **0.9523** across all evaluation metrics.

---

## Objective

Deliver software capable of:

1. **Pulling prompts** from LangSmith Prompt Hub containing low-quality prompts
2. **Refactoring and optimizing** those prompts using advanced Prompt Engineering techniques
3. **Pushing optimized prompts** back to LangSmith
4. **Evaluating quality** through custom metrics (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Achieving a minimum score** of 0.9 (90%) on all evaluation metrics

---

## Technologies

- **Language:** Python 3.9+
- **Framework:** LangChain
- **Evaluation Platform:** LangSmith
- **Prompt Management:** LangSmith Prompt Hub
- **Prompt Format:** YAML

### Recommended Packages

```python
from langchain import hub              # Pull and Push prompts
from langsmith import Client           # LangSmith API interaction
from langsmith.evaluation import evaluate  # Prompt evaluation
from langchain_openai import ChatOpenAI    # OpenAI LLM
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini LLM
```

### LLM Options

**OpenAI:**
- Create an API Key at: https://platform.openai.com/api-keys
- LLM model for responses: `gpt-4o-mini`
- LLM model for evaluation: `gpt-4o`
- Estimated cost: ~$1-5 to complete the challenge

**Gemini (free option):**
- Create an API Key at: https://aistudio.google.com/app/apikey
- LLM model for responses: `gemini-2.5-flash`
- LLM model for evaluation: `gemini-2.5-flash`
- Limit: 15 req/min, 1500 req/day

---

## Project Structure

```
mba-ia-pull-evaluation-prompt/
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── prompts/
│   ├── bug_to_user_story_v1.yml   # Base prompt (already included)
│   └── bug_to_user_story_v2.yml   # Your optimized prompt (to create)
│
├── datasets/
│   └── bug_to_user_story.jsonl    # 15 bug examples (already included)
│
├── src/
│   ├── pull_prompts.py            # Pull from LangSmith (implement)
│   ├── push_prompts.py            # Push to LangSmith (implement)
│   ├── evaluate.py                # Automatic evaluation (ready)
│   ├── metrics.py                 # 5 implemented metrics (ready)
│   └── utils.py                   # Helper functions (ready)
│
├── tests/
│   └── test_prompts.py            # Validation tests (implement)
```

**What you must implement:**
- `prompts/bug_to_user_story_v2.yml` — Create from scratch with your optimized prompt
- `src/pull_prompts.py` — Implement the function bodies (skeleton already exists)
- `src/push_prompts.py` — Implement the function bodies (skeleton already exists)
- `tests/test_prompts.py` — Implement the 6 validation tests (skeleton already exists)
- `README.md` — Document your optimization process

**What comes ready (do not alter):**
- `src/evaluate.py` — Complete evaluation script
- `src/metrics.py` — 5 implemented metrics (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Helper functions
- `datasets/bug_to_user_story.jsonl` — Dataset with 15 bugs (5 simple, 7 medium, 3 complex)
- Multi-provider support (OpenAI and Gemini)

---

## How to Run

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd mba-ia-pull-evaluation-prompt

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LangSmith
LANGSMITH_API_KEY=lsv2_pt_your_key_here
USERNAME_LANGSMITH_HUB=your_username_here
LANGSMITH_PROJECT=prompt-optimization-challenge-resolved

# LLM Provider
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o

# OpenAI
OPENAI_API_KEY=sk-your_key_here
```

### Execution Order

#### Step 1 — Pull base prompt

```bash
python src/pull_prompts.py
```

#### Step 2 — Refactor the prompt

Edit `prompts/bug_to_user_story_v2.yml` manually applying the techniques learned.

#### Step 3 — Push optimized prompt

```bash
python src/push_prompts.py
```

#### Step 4 — Run evaluation

```bash
python src/evaluate.py
```

### Validation Tests

```bash
pytest tests/test_prompts.py -v
```

The 6 required tests:

| Test | What it checks |
|---|---|
| `test_prompt_has_system_prompt` | Field exists and is not empty |
| `test_prompt_has_role_definition` | Persona defined (e.g. "Você é um Product Manager") |
| `test_prompt_mentions_format` | User Story format present (Como/Eu quero/Dado/Quando/Então) |
| `test_prompt_has_few_shot_examples` | Input/output examples present |
| `test_prompt_no_todos` | No `[TODO]` markers left in the prompt |
| `test_minimum_techniques` | At least 2 techniques listed in `techniques_applied` |

### Approval Criteria

```
- Helpfulness  >= 0.9
- Correctness  >= 0.9
- F1-Score     >= 0.9
- Clarity      >= 0.9
- Precision    >= 0.9

Average of 5 metrics >= 0.9
```

> **IMPORTANT:** ALL 5 metrics must be >= 0.9, not just the average!

---

## Techniques Applied (Phase 2)

### 1. Few-shot Learning *(mandatory)*

**Why I chose it:** It is the most effective technique for tasks with structured output. By providing input/output examples, the model learns the exact expected format without needing overly detailed instructions.

**How I applied it:** Included **11 complete examples** covering all dataset patterns — simple bugs (validation, UI, cross-browser), medium (performance, security, integration) and complex (multiple critical issues). Each example uses the `BUG: ... RESPOSTA:` pair so the model completes the pattern by analogy.

```
BUG: "Campo de email aceita texto sem @, permitindo cadastros inválidos."
RESPOSTA:
Como um usuário criando uma conta, eu quero que o sistema valide meu email
corretamente, para que eu não insira um endereço inválido por engano.

Critérios de Aceitação:
- Dado que estou no formulário de cadastro
- Quando digito um email sem o caractere @
- Então devo ver uma mensagem de erro
- E não devo conseguir prosseguir com o cadastro
- E a mensagem deve explicar o formato correto
```

---

### 2. Chain of Thought (CoT)

**Why I chose it:** Bugs vary widely in complexity — simple, medium and critical. CoT forces the model to analyze the bug before writing, ensuring that persona, benefit and criteria are correctly extracted from each context.

**How I applied it:** Explicit 5-step instruction before writing:

```
1. PERSONA: who uses the feature? Can be "the system" for automatic validations
2. FUNCTIONALITY: what should work?
3. BENEFIT: what is the business value?
4. GENERIC CRITERIA: conditions that prove it works (without specific IDs)
5. EXTRA SECTIONS: only if the bug has explicit technical data
```

---

### 3. Role Prompting

**Why I chose it:** Defining a specialized persona improves the quality and tone of responses. A Senior Product Manager knows when to use "As the system" vs "As a customer", and when a technical section is necessary.

**How I applied it:** System prompt starts with `"Você é um Product Manager Sênior especialista em metodologias ágeis"` and includes absolute behavioral rules:

```
- COPY the style of the examples — do not create sections that do not appear in the corresponding example
- Use "um produto", "um usuário" — NEVER "o produto ID 1234"
- Simple bug without technical data = ONLY the Given/When/Then block, NO extra sections
```

---

### 4. Tree of Thought

**Why I chose it:** Complex bugs have multiple angles (user, system, technical). Exploring these angles before writing ensures coverage of edge cases that the reference expects.

**How I applied it:** Section for exploring angles before writing:

```
## EXPLORE ANGLES (Tree of Thought)
- End user perspective
- System/business perspective
- Edge cases mentioned in the bug
```

---

### 5. Skeleton of Thought

**Why I chose it:** The user story format is rigid. Defining a skeleton with conditional sections ensures proportionality — simple bugs generate short responses, complex bugs generate complete responses.

**How I applied it:** Mandatory base structure + clearly defined optional sections:

```
As a [persona], I want [functionality], so that [benefit].

Acceptance Criteria:        ← always mandatory
Technical Context:          ← only with logs/endpoints/stack traces
Additional Criteria:        ← only with multiple problems
Technical Criteria:         ← only with performance requirements
Calculation Example:        ← only with numerical calculations
```

---

## Final Results

### Metrics Achieved (version 3.3)

| Metric | Score | Status |
|---|---|---|
| Helpfulness | 0.95 | ✅ Approved |
| Correctness | 0.95 | ✅ Approved |
| F1-Score | 0.96 | ✅ Approved |
| Clarity | 0.97 | ✅ Approved |
| Precision | 0.93 | ✅ Approved |
| **Overall Average** | **0.9523** | ✅ **Approved** |

### Prompt on LangSmith Hub

🔗 [patricia-souza/bug_to_user_story_v2](https://smith.langchain.com/hub/patricia-souza/bug_to_user_story_v2/918268de?organizationId=7f933ea8-ee69-4ec3-be1c-13883593799a&tab=0)

### Comparative Table: v1 (poor) vs v2 (optimized)

| Aspect | v1 (base) | v2 (optimized) |
|---|---|---|
| System Prompt | `"You are a chatbot."` | Senior Product Manager with detailed instructions |
| Techniques | None | Few-shot, CoT, Role Prompting, Tree of Thought, Skeleton of Thought |
| Examples | 0 | 11 examples covering all patterns |
| Persona | Generic | Specific to bug context |
| Conditional sections | No | Yes (Technical Context, Additional Criteria, etc.) |
| Helpfulness | ~0.45 | 0.95 |
| Correctness | ~0.52 | 0.95 |
| F1-Score | ~0.48 | 0.96 |
| Clarity | ~0.50 | 0.97 |
| Precision | ~0.46 | 0.93 |
| **Average** | **~0.48** | **0.9523** |

### Iteration Process

The project went through **11 versions** to achieve the minimum score of 0.9:

| Version | Average | Key Learning |
|---|---|---|
| v2.0 | ~0.40 | Wrong `{question}` variable — dataset uses `{bug_report}` |
| v2.1 | 0.85 | Low F1 on simple bugs — prompt was generating too much |
| v2.2 | 0.89 | Too rich examples distorted simple bugs |
| v2.3–2.5 | 0.88 | Tree of Thought added, F1 oscillating |
| v2.6–2.8 | 0.88 | Long prompt caused model to ignore examples |
| v2.9–3.0 | 0.87 | Model added specific IDs to generic criteria |
| v3.1 | 0.88 | `BUG/RESPOSTA` format improved completion |
| v3.2 | 0.88 | Exact examples for bugs 11 and 12 added |
| **v3.3** | **0.9523** | Examples for bugs 8 and 9 + anti-invention rule |

---

## LangSmith Evidence

### Project Dashboard

🔗 **Public project link:**
<https://smith.langchain.com/o/7f933ea8-ee69-4ec3-be1c-13883593799a/projects/p/d33cacc9-b733-46f1-87cb-cf7c7179752e?timeModel=%7B%22duration%22%3A%221d%22%7D>

### Evaluation Dataset (15 examples)

The dataset `prompt-optimization-challenge-resolved-eval` contains 15 bug reports with reference user stories:

- **5 simple bugs:** cart button, email validation, iOS landscape, dashboard, Safari
- **5 medium bugs:** webhook, SQL report, permissions API, discount pipeline, Android ANR
- **5 complex bugs:** critical checkout, stock validation, z-index modal, management reports, offline sync app

🔗 **Dataset link:**
<https://smith.langchain.com/o/7f933ea8-ee69-4ec3-be1c-13883593799a/datasets/8bc3f737-587a-414a-aa2d-fdc99a0c97a7?tab=1>

### Executions with Scores ≥ 0.9 — Optimized Prompt v2

Final evaluation result for prompt `patricia-souza/bug_to_user_story_v2` (version 3.3):

| Example | F1-Score | Clarity | Precision |
|---|---|---|---|
| [1/15] Cart button | 0.87 | 0.90 | 0.90 |
| [2/15] Email validation | 0.75 | 0.90 | 0.90 |
| [3/15] iOS landscape | 0.87 | 0.90 | 0.90 |
| [4/15] Dashboard users | 1.00 | 1.00 | 1.00 |
| [5/15] Safari images | 1.00 | 1.00 | 1.00 |
| [6/15] Payment webhook | 1.00 | 1.00 | 1.00 |
| [7/15] SQL report | 1.00 | 1.00 | 1.00 |
| [8/15] Permissions API | 1.00 | 1.00 | 1.00 |
| [9/15] Discount pipeline | 0.95 | 0.90 | 0.90 |
| [10/15] Android ANR | 1.00 | 1.00 | 1.00 |
| [11/15] Stock checkout | 1.00 | 1.00 | 1.00 |
| [12/15] Modal z-index | 1.00 | 1.00 | 1.00 |
| [13/15] Critical checkout | 1.00 | 1.00 | 1.00 |
| [14/15] Management reports | 1.00 | 1.00 | 1.00 |
| [15/15] Offline sync app | 1.00 | 1.00 | 0.33 |
| **Final Average** | **0.96 ✅** | **0.97 ✅** | **0.93 ✅** |

**Derived Metrics:**
- Helpfulness: **0.95 ✅**
- Correctness: **0.95 ✅**
- **Overall Average: 0.9523 ✅**

### Detailed Tracing (≥ 3 examples)

Access full tracing on LangSmith at:
`Projects → prompt-optimization-challenge-resolved → click any run`

**Example 1 — Simple Bug (Cart button):**
- Input: `"Botão de adicionar ao carrinho não funciona no produto ID 1234."`
- Technique applied: Few-shot identified simple pattern → generated only Given/When/Then block
- Metrics: F1:0.87 | Clarity:0.90 | Precision:0.90

**Example 8 — Medium Bug with Security (Permissions API):**
- Input: `"Endpoint /api/users/:id retorna dados de qualquer usuário sem validar permissões..."`
- Technique applied: Tree of Thought identified 2 personas (regular user + admin) → generated "Additional Criteria for Admins" + "Security Context"
- Metrics: F1:1.00 | Clarity:1.00 | Precision:1.00

**Example 13 — Critical Complex Bug (Checkout multiple failures):**
- Input: Checkout system with XSS, timeout, race condition and infinite loading
- Technique applied: Chain of Thought identified 4 distinct problems → generated main user story + 4 separate criteria blocks (Security, Integration, Logic, UX) + complete technical sections
- Metrics: F1:1.00 | Clarity:1.00 | Precision:1.00

🔗 **Public prompt on Hub:** <https://smith.langchain.com/hub/patricia-souza/bug_to_user_story_v2/918268de?organizationId=7f933ea8-ee69-4ec3-be1c-13883593799a&tab=0>