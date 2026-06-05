"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Campos obrigatórios
    required_fields = ["description", "system_prompt", "version"]
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: '{field}'")

    # Validar conteúdo do system_prompt
    system_prompt = prompt_data.get("system_prompt", "").strip()
    if not system_prompt:
        errors.append("'system_prompt' está vazio")

    if "TODO" in system_prompt:
        errors.append("'system_prompt' ainda contém TODOs não resolvidos")

    # Validar técnicas aplicadas (mínimo 2)
    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(
            f"Mínimo de 2 técnicas requeridas em 'techniques_applied', encontradas: {len(techniques)}"
        )

    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no formato 'username/nome-do-prompt'
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    print(f"\nFazendo push: {prompt_name}")

    # --- Validar antes de enviar ---
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for err in errors:
            print(f"   - {err}")
        return False

    print("   ✓ Validação passou")

    # --- Montar ChatPromptTemplate ---
    system_prompt_text = prompt_data.get("system_prompt", "").strip()
    user_prompt_text = prompt_data.get("user_prompt", "{question}").strip()

    try:
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt_text),
            HumanMessagePromptTemplate.from_template(user_prompt_text),
        ])
    except Exception as e:
        print(f"❌ Erro ao montar ChatPromptTemplate: {e}")
        return False

    # --- Push para o Hub ---
    try:
        techniques = prompt_data.get("techniques_applied", [])
        description = prompt_data.get("description", "Prompt otimizado")
        tags = [t.lower().replace(" ", "-") for t in techniques] + ["optimized", "v2"]

        hub.push(
            prompt_name,
            prompt_template,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=tags,
        )

        print(f"   ✓ Push realizado com sucesso!")
        print(f"   ✓ Técnicas: {', '.join(techniques)}")
        print(f"   ✓ Tags: {', '.join(tags)}")
        print(f"   🔗 URL: https://smith.langchain.com/hub/{prompt_name}")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erro ao fazer push para o Hub: {error_msg}")

        if "401" in error_msg or "unauthorized" in error_msg.lower():
            print("\n   Verifique se LANGSMITH_API_KEY está correta no .env")
        elif "not found" in error_msg.lower() or "404" in error_msg:
            print("\n   O repositório não existe ainda — será criado automaticamente.")
            print("   Se o erro persistir, verifique o USERNAME_LANGSMITH_HUB no .env")

        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS PARA O LANGSMITH HUB")

    # Checar variáveis obrigatórias
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()

    # Arquivo YAML com o prompt otimizado
    yaml_path = "prompts/bug_to_user_story_v2.yml"
    print(f"Carregando prompt de: {yaml_path}")

    prompt_data = load_yaml(yaml_path)
    if prompt_data is None:
        print(f"\n❌ Não foi possível carregar '{yaml_path}'.")
        print("   Certifique-se de ter criado o arquivo com o prompt otimizado.")
        return 1

    print("   ✓ Arquivo carregado")

    # Nome final no Hub: username/bug_to_user_story_v2
    prompt_name = f"{username}/bug_to_user_story_v2"


    success = push_prompt_to_langsmith(prompt_name, prompt_data)

    if success:
        print("\n" + "=" * 50)
        print("✅ Push concluído com sucesso!")
        print("=" * 50)
        print("\nPróximos passos:")
        print(f"1. Confirme em: https://smith.langchain.com/prompts")
        print(f"2. Execute a avaliação: python src/evaluate.py")
        return 0
    else:
        print("\n❌ Push falhou. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())