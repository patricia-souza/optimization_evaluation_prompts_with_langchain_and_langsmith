"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Tenta pull do prompt leonanluppi/bug_to_user_story_v1 do Hub
2. Se não conseguir (prompt privado/403), cria o v1 localmente como fallback
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

# Conteúdo do prompt v1 (baixa qualidade — ponto de partida do exercício)
FALLBACK_V1_PROMPT = {
    "description": "Prompt de baixa qualidade para converter bug reports em user stories (v1 - base para otimização)",
    "version": "1.0",
    "source": "leonanluppi/bug_to_user_story_v1",
    "system_prompt": "You are a chatbot.",
    "user_prompt": "{question}",
    "techniques_applied": [],
    "notes": (
        "Prompt original de baixa qualidade. "
        "Sem instruções claras, sem exemplos, sem estrutura definida. "
        "Criado localmente pois o prompt original está privado no Hub."
    ),
}


def pull_prompts_from_langsmith():
    """
    Tenta fazer pull do prompt do LangSmith Hub.
    Se falhar (403/privado), usa fallback local.

    Returns:
        True se sucesso, False caso contrário
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return False

    prompt_repo = "leonanluppi/bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"

    # --- Tentar pull real ---
    print(f"Tentando pull do prompt: {prompt_repo}")
    try:
        prompt = hub.pull(prompt_repo)
        print("   ✓ Prompt carregado do Hub com sucesso")

        system_prompt = ""
        user_prompt = "{question}"

        try:
            for msg in prompt.messages:
                role = msg.__class__.__name__.lower()
                content = msg.prompt.template if hasattr(msg, "prompt") else str(msg)
                if "system" in role:
                    system_prompt = content
                elif "human" in role:
                    user_prompt = content
        except Exception:
            pass

        prompt_data = {
            "description": "Prompt base baixado do LangSmith Hub (v1)",
            "version": "1.0",
            "source": prompt_repo,
            "system_prompt": system_prompt or "You are a chatbot.",
            "user_prompt": user_prompt,
            "techniques_applied": [],
            "notes": "Prompt original baixado do LangSmith Hub.",
        }

    except Exception as e:
        error_str = str(e)

        if "403" in error_str or "Forbidden" in error_str:
            print(f"   ⚠️  Prompt '{prompt_repo}' está privado (403 Forbidden).")
            print("   → Usando conteúdo padrão v1 como fallback (comportamento esperado).")
        elif "404" in error_str or "not found" in error_str.lower():
            print(f"   ⚠️  Prompt '{prompt_repo}' não encontrado.")
            print("   → Usando conteúdo padrão v1 como fallback.")
        else:
            print(f"   ⚠️  Erro ao fazer pull: {e}")
            print("   → Usando conteúdo padrão v1 como fallback.")

        prompt_data = FALLBACK_V1_PROMPT

    # --- Salvar localmente ---
    if save_yaml(prompt_data, output_path):
        print(f"   ✓ Arquivo salvo em: {output_path}")
        return True
    else:
        print(f"❌ Falha ao salvar: {output_path}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()

    if success:
        print("\n" + "=" * 50)
        print("✅ Pull concluído com sucesso!")
        print("=" * 50)
        print("\nPróximos passos:")
        print("1. Analise: prompts/bug_to_user_story_v1.yml")
        print("2. Crie:    prompts/bug_to_user_story_v2.yml  (versão otimizada)")
        print("3. Execute: python src/push_prompts.py")
        return 0
    else:
        print("\n❌ Pull falhou. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())