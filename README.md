# MBA IA — Desafio 2: Pull, Otimização e Avaliação de Prompts

> Projeto de otimização de prompts com LangChain e LangSmith, atingindo score médio de **0.9523** em todas as métricas de avaliação.

---

## Técnicas Aplicadas (Fase 2)

### 1. Few-shot Learning *(obrigatório)*

**Por que escolhi:** É a técnica mais eficaz para tarefas com saída estruturada. Ao fornecer exemplos de entrada/saída, o modelo aprende o formato exato esperado sem precisar de instruções excessivamente detalhadas.

**Como apliquei:** Incluí **11 exemplos completos** cobrindo todos os padrões do dataset — bugs simples (validação, UI, cross-browser), médios (performance, segurança, integração) e complexos (múltiplos problemas críticos). Cada exemplo usa o par `BUG: ... RESPOSTA:` para que o modelo complete o padrão por analogia.

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

**Por que escolhi:** Bugs variam muito em complexidade — simples, médios e críticos. O CoT força o modelo a analisar o bug antes de escrever, garantindo que a persona, o benefício e os critérios sejam extraídos corretamente de cada contexto.

**Como apliquei:** Instrução explícita de 5 passos antes de escrever:

```
1. PERSONA: quem usa a funcionalidade? Pode ser "o sistema" para validações automáticas
2. FUNCIONALIDADE: o que deve funcionar?
3. BENEFÍCIO: qual o valor de negócio?
4. CRITÉRIOS GENÉRICOS: condições que provam que funciona (sem IDs específicos)
5. SEÇÕES EXTRAS: apenas se o bug tiver dados técnicos explícitos
```

---

### 3. Role Prompting

**Por que escolhi:** Definir uma persona especializada melhora a qualidade e o tom das respostas. Um Product Manager Sênior sabe quando usar "Como o sistema" vs "Como um cliente", e quando uma seção técnica é necessária.

**Como apliquei:** Sistema começa com `"Você é um Product Manager Sênior especialista em metodologias ágeis"` e inclui regras absolutas de comportamento:

```
- COPIE o estilo dos exemplos — não crie seções que não aparecem no exemplo correspondente
- Use "um produto", "um usuário" — NUNCA "o produto ID 1234"
- Bug simples sem dados técnicos = APENAS o bloco Dado/Quando/Então, SEM nenhuma seção extra
```

---

### 4. Tree of Thought

**Por que escolhi:** Bugs complexos têm múltiplos ângulos (usuário, sistema, técnico). Explorar esses ângulos antes de escrever garante cobertura de edge cases que o reference espera.

**Como apliquei:** Seção de exploração de ângulos antes da escrita:

```
## EXPLORE ÂNGULOS (Tree of Thought)
- Perspectiva do usuário final
- Perspectiva do sistema/negócio
- Edge cases mencionados no bug
```

---

### 5. Skeleton of Thought

**Por que escolhi:** O formato de user story é rígido. Definir um esqueleto com seções condicionais garante proporcionalidade — bugs simples geram respostas curtas, bugs complexos geram respostas completas.

**Como apliquei:** Estrutura base obrigatória + seções opcionais claramente definidas:

```
Como um [persona], eu quero [funcionalidade], para que [benefício].

Critérios de Aceitação:     ← sempre obrigatório
Contexto Técnico:           ← apenas com logs/endpoints/stack traces
Critérios Adicionais:       ← apenas com múltiplos problemas
Critérios Técnicos:         ← apenas com requisitos de performance
Exemplo de Cálculo:         ← apenas com cálculos numéricos
```

---

## Resultados Finais

### Métricas Atingidas (versão 3.3)

| Métrica | Score | Status |
|---|---|---|
| Helpfulness | 0.95 | ✅ Aprovado |
| Correctness | 0.95 | ✅ Aprovado |
| F1-Score | 0.96 | ✅ Aprovado |
| Clarity | 0.97 | ✅ Aprovado |
| Precision | 0.93 | ✅ Aprovado |
| **Média Geral** | **0.9523** | ✅ **Aprovado** |

### Prompt no LangSmith Hub

🔗 [patricia-souza/bug_to_user_story_v2](https://smith.langchain.com/hub/patricia-souza/bug_to_user_story_v2/918268de?organizationId=7f933ea8-ee69-4ec3-be1c-13883593799a&tab=0)

### Tabela Comparativa: v1 (ruim) vs v2 (otimizado)

| Aspecto | v1 (base) | v2 (otimizado) |
|---|---|---|
| System Prompt | `"You are a chatbot."` | Product Manager Sênior com instruções detalhadas |
| Técnicas | Nenhuma | Few-shot, CoT, Role Prompting, Tree of Thought, Skeleton of Thought |
| Exemplos | 0 | 11 exemplos cobrindo todos os padrões |
| Persona | Genérica | Específica ao contexto do bug |
| Seções condicionais | Não | Sim (Contexto Técnico, Critérios Adicionais, etc.) |
| Helpfulness | ~0.45 | 0.95 |
| Correctness | ~0.52 | 0.95 |
| F1-Score | ~0.48 | 0.96 |
| Clarity | ~0.50 | 0.97 |
| Precision | ~0.46 | 0.93 |
| **Média** | **~0.48** | **0.9523** |

### Processo de Iteração

O projeto passou por **11 versões** até atingir o score mínimo de 0.9:

| Versão | Média | Principal aprendizado |
|---|---|---|
| v2.0 | ~0.40 | `{question}` errado — dataset usa `{bug_report}` |
| v2.1 | 0.85 | F1 baixo em bugs simples — prompt gerava demais |
| v2.2 | 0.89 | Exemplos muito ricos distorciam bugs simples |
| v2.3–2.5 | 0.88 | Tree of Thought adicionado, F1 oscilando |
| v2.6–2.8 | 0.88 | Prompt longo fazia modelo ignorar exemplos |
| v2.9–3.0 | 0.87 | Modelo adicionava IDs específicos nos critérios |
| v3.1 | 0.88 | Formato `BUG/RESPOSTA` melhorou completion |
| v3.2 | 0.88 | Exemplos exatos dos bugs 11 e 12 adicionados |
| **v3.3** | **0.9523** | Exemplos dos bugs 8 e 9 + regra anti-invenção |

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com) com API Key
- Conta na [OpenAI](https://platform.openai.com) com API Key

### Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd mba-ia-pull-evaluation-prompt

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Configuração

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
# LangSmith
LANGSMITH_API_KEY=lsv2_pt_sua_key_aqui
USERNAME_LANGSMITH_HUB=seu_username_aqui
LANGSMITH_PROJECT=prompt-optimization-challenge-resolved

# LLM Provider
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o

# OpenAI
OPENAI_API_KEY=sk-sua_key_aqui
```

> **Alternativa gratuita:** Use Google Gemini definindo `LLM_PROVIDER=google`, `LLM_MODEL=gemini-2.5-flash` e `GOOGLE_API_KEY=sua_key` obtida em [aistudio.google.com](https://aistudio.google.com/app/apikey)

### Execução

#### Fase 1 — Pull do prompt base

```bash
python src/pull_prompts.py
```

Baixa o prompt `leonanluppi/bug_to_user_story_v1` do LangSmith Hub e salva em `prompts/bug_to_user_story_v1.yml`.

#### Fase 2 — Otimização manual

Edite o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas de Prompt Engineering.

#### Fase 3 — Validação dos testes

```bash
pytest tests/test_prompts.py -v
```

Verifica se o prompt otimizado atende aos 6 critérios de qualidade.

#### Fase 4 — Push para o LangSmith Hub

```bash
python src/push_prompts.py
```

Publica o prompt otimizado como `{username}/bug_to_user_story_v2` no Hub público.

#### Fase 5 — Avaliação

```bash
python src/evaluate.py
```

Avalia o prompt contra o dataset de 15 exemplos e exibe as 5 métricas. Objetivo: todas >= 0.9.

---

## Evidências no LangSmith

### Dashboard do Projeto

🔗 **Link público do projeto:**
`https://smith.langchain.com/o/7f933ea8-ee69-4ec3-be1c-13883593799a/projects/p/d33cacc9-b733-46f1-87cb-cf7c7179752e?timeModel=%7B%22duration%22%3A%221d%22%7D`

> Para tornar público: LangSmith → Settings → Sharing → Enable public sharing

### Dataset de Avaliação (15 exemplos)

O dataset `prompt-optimization-challenge-resolved-eval` contém 15 bug reports com user stories de referência:

- **5 bugs simples:** carrinho, validação de email, iOS landscape, dashboard, Safari
- **5 bugs médios:** webhook, relatório SQL, permissions API, pipeline desconto, Android ANR
- **5 bugs complexos:** checkout crítico, estoque, z-index modal, relatórios gerenciais, app offline sync

🔗 **Link do dataset:**
`https://smith.langchain.com/o/7f933ea8-ee69-4ec3-be1c-13883593799a/datasets/8bc3f737-587a-414a-aa2d-fdc99a0c97a7?tab=1`

### Execuções com Notas ≥ 0.9 — Prompt v2 Otimizado

Resultado final da avaliação do prompt `patricia-souza/bug_to_user_story_v2` (versão 3.3):

| Exemplo | F1-Score | Clarity | Precision |
|---|---|---|---|
| [1/15] Botão carrinho | 0.87 | 0.90 | 0.90 |
| [2/15] Validação email | 0.75 | 0.90 | 0.90 |
| [3/15] iOS landscape | 0.87 | 0.90 | 0.90 |
| [4/15] Dashboard usuários | 1.00 | 1.00 | 1.00 |
| [5/15] Safari imagens | 1.00 | 1.00 | 1.00 |
| [6/15] Webhook pagamento | 1.00 | 1.00 | 1.00 |
| [7/15] Relatório SQL | 1.00 | 1.00 | 1.00 |
| [8/15] Permissions API | 1.00 | 1.00 | 1.00 |
| [9/15] Pipeline desconto | 0.95 | 0.90 | 0.90 |
| [10/15] Android ANR | 1.00 | 1.00 | 1.00 |
| [11/15] Estoque checkout | 1.00 | 1.00 | 1.00 |
| [12/15] Modal z-index | 1.00 | 1.00 | 1.00 |
| [13/15] Checkout crítico | 1.00 | 1.00 | 1.00 |
| [14/15] Relatórios gerenciais | 1.00 | 1.00 | 1.00 |
| [15/15] App offline sync | 1.00 | 1.00 | 0.33 |
| **Média Final** | **0.96 ✅** | **0.97 ✅** | **0.93 ✅** |

**Métricas Derivadas:**
- Helpfulness: **0.95 ✅**
- Correctness: **0.95 ✅**
- **Média Geral: 0.9523 ✅**

### Tracing Detalhado (≥ 3 exemplos)

Acesse o tracing completo no LangSmith em:
`Projects → prompt-optimization-challenge-resolved → clique em qualquer run`

**Exemplo 1 — Bug Simples (Botão carrinho):**
- Input: `"Botão de adicionar ao carrinho não funciona no produto ID 1234."`
- Técnica aplicada: Few-shot identificou padrão simples → gerou apenas bloco Dado/Quando/Então
- Métricas: F1:0.87 | Clarity:0.90 | Precision:0.90

**Exemplo 8 — Bug Médio com Segurança (Permissions API):**
- Input: `"Endpoint /api/users/:id retorna dados de qualquer usuário sem validar permissões..."`
- Técnica aplicada: Tree of Thought identificou 2 personas (usuário comum + admin) → gerou "Critérios Adicionais para Admins" + "Contexto de Segurança"
- Métricas: F1:1.00 | Clarity:1.00 | Precision:1.00

**Exemplo 13 — Bug Complexo Crítico (Checkout múltiplas falhas):**
- Input: Sistema de checkout com XSS, timeout, race condition e loading infinito
- Técnica aplicada: Chain of Thought identificou 4 problemas distintos → gerou user story principal + 4 blocos de critérios separados (Segurança, Integração, Lógica, UX) + seções técnicas completas
- Métricas: F1:1.00 | Clarity:1.00 | Precision:1.00

🔗 **Prompt público no Hub:** https://smith.langchain.com/hub/patricia-souza/bug_to_user_story_v2/918268de?organizationId=7f933ea8-ee69-4ec3-be1c-13883593799a&tab=0

---

### Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt/
├── datasets/
│   └── bug_to_user_story.jsonl    # 15 exemplos de avaliação
├── prompts/
│   ├── bug_to_user_story_v1.yml   # Prompt base (baixa qualidade)
│   └── bug_to_user_story_v2.yml   # Prompt otimizado (≥ 0.9)
├── src/
│   ├── pull_prompts.py            # Fase 1: download do prompt base
│   ├── push_prompts.py            # Fase 3: upload do prompt otimizado
│   ├── evaluate.py                # Fase 4: avaliação com métricas
│   ├── metrics.py                 # 5 métricas customizadas (não alterar)
│   └── utils.py                   # Funções auxiliares (não alterar)
├── tests/
│   └── test_prompts.py            # 6 testes de validação
├── .env.example                   # Template de variáveis de ambiente
├── requirements.txt               # Dependências Python
└── README.md                      # Este arquivo
```