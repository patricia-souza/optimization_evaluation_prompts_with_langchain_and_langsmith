"""
Testes de validação para o prompt otimizado bug_to_user_story_v2.yml

Execução:
    pytest tests/test_prompts.py -v
"""

import pytest
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# Fixture: carrega o YAML uma única vez para todos os testes
# ---------------------------------------------------------------------------

PROMPT_PATH = Path("prompts/bug_to_user_story_v2.yml")


@pytest.fixture(scope="module")
def prompt_data():
    """Carrega e retorna o conteúdo do arquivo YAML do prompt v2."""
    assert PROMPT_PATH.exists(), (
        f"Arquivo não encontrado: {PROMPT_PATH}\n"
        "Execute primeiro: python src/pull_prompts.py && crie prompts/bug_to_user_story_v2.yml"
    )
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, "Arquivo YAML está vazio ou malformado"
    return data


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def test_prompt_has_system_prompt(prompt_data):
    """
    Verifica se o campo 'system_prompt' existe e não está vazio.
    """
    assert "system_prompt" in prompt_data, (
        "Campo 'system_prompt' não encontrado no YAML"
    )
    system_prompt = prompt_data["system_prompt"]
    assert isinstance(system_prompt, str), (
        "'system_prompt' deve ser uma string"
    )
    assert system_prompt.strip(), (
        "'system_prompt' está vazio ou contém apenas espaços"
    )
    assert len(system_prompt.strip()) >= 50, (
        f"'system_prompt' muito curto ({len(system_prompt.strip())} chars). "
        "Um prompt útil deve ter pelo menos 50 caracteres."
    )


def test_prompt_has_role_definition(prompt_data):
    """
    Verifica se o prompt define uma persona clara
    (ex: 'Você é um Product Manager', 'You are a...').
    """
    system_prompt = prompt_data.get("system_prompt", "")

    role_indicators = [
        "você é",
        "voce é",
        "você e um",
        "you are",
        "seu papel",
        "sua função",
        "especialista",
        "sênior",
        "senior",
        "product manager",
        "agile",
        "ágil",
    ]

    found_role = any(
        indicator in system_prompt.lower()
        for indicator in role_indicators
    )

    assert found_role, (
        "O prompt não define uma persona/role clara.\n"
        "Adicione algo como: 'Você é um Product Manager Sênior especialista em...'\n"
        f"Trecho atual (primeiros 200 chars): {system_prompt[:200]}"
    )


def test_prompt_mentions_format(prompt_data):
    """
    Verifica se o prompt exige formato Markdown ou User Story padrão
    (Como / Eu quero / Para que).
    """
    system_prompt = prompt_data.get("system_prompt", "")
    prompt_lower = system_prompt.lower()

    format_indicators = [
        "como um",
        "eu quero",
        "para que",
        "as a",
        "i want",
        "so that",
        "markdown",
        "formato",
        "user story",
        "critérios de aceitação",
        "criterios de aceitacao",
        "acceptance criteria",
        "dado que",
        "quando",
        "então",
    ]

    found_format = any(
        indicator in prompt_lower
        for indicator in format_indicators
    )

    assert found_format, (
        "O prompt não menciona o formato esperado de User Story ou Markdown.\n"
        "Inclua instruções de formato como:\n"
        "  'Como um [usuário], Eu quero [ação], Para que [benefício]'\n"
        "  ou referência a critérios de aceitação (Dado/Quando/Então)."
    )


def test_prompt_has_few_shot_examples(prompt_data):
    """
    Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
    Critérios: pelo menos 1 bloco de exemplo com input e output representados.
    """
    system_prompt = prompt_data.get("system_prompt", "")
    prompt_lower = system_prompt.lower()

    few_shot_indicators = [
        "exemplo",
        "example",
        "bug report:",
        "user story gerada",
        "entrada:",
        "saída:",
        "input:",
        "output:",
        "---",          # separador de exemplos
    ]

    matches = sum(
        1 for indicator in few_shot_indicators
        if indicator in prompt_lower
    )

    assert matches >= 2, (
        f"O prompt não parece conter exemplos Few-shot (encontrados {matches} indicadores).\n"
        "Adicione pelo menos 1 exemplo completo de Bug Report → User Story.\n"
        "Use marcadores como 'Exemplo:', '---', 'Bug Report:', 'User Story Gerada:'"
    )


def test_prompt_no_todos(prompt_data):
    """
    Garante que não existem marcadores [TODO] ou # TODO no prompt.
    """
    system_prompt = prompt_data.get("system_prompt", "")
    user_prompt = prompt_data.get("user_prompt", "")
    description = prompt_data.get("description", "")

    fields_to_check = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "description": description,
    }

    todos_found = []
    for field_name, content in fields_to_check.items():
        if content and "TODO" in str(content).upper():
            todos_found.append(field_name)

    assert not todos_found, (
        f"TODOs encontrados nos campos: {', '.join(todos_found)}\n"
        "Remova todos os marcadores [TODO] antes de usar o prompt em produção."
    )


def test_minimum_techniques(prompt_data):
    """
    Verifica (através dos metadados do YAML) se pelo menos 2 técnicas
    de Prompt Engineering foram listadas em 'techniques_applied'.
    """
    assert "techniques_applied" in prompt_data, (
        "Campo 'techniques_applied' não encontrado no YAML.\n"
        "Adicione uma lista com as técnicas usadas, ex:\n"
        "  techniques_applied:\n"
        "    - 'Few-shot Learning'\n"
        "    - 'Chain of Thought (CoT)'"
    )

    techniques = prompt_data["techniques_applied"]

    assert isinstance(techniques, list), (
        "'techniques_applied' deve ser uma lista YAML"
    )

    assert len(techniques) >= 2, (
        f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}.\n"
        f"Técnicas atuais: {techniques}\n"
        "Adicione pelo menos mais uma técnica à lista 'techniques_applied'."
    )

    # Garantir que os itens são strings não vazias
    valid_techniques = [t for t in techniques if isinstance(t, str) and t.strip()]
    assert len(valid_techniques) >= 2, (
        f"Técnicas válidas (strings não vazias): {valid_techniques}\n"
        "Certifique-se de que os itens da lista são strings com conteúdo."
    )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])