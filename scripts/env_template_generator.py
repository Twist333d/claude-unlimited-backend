import os
from pathlib import Path
from colorama import init, Fore, Style

init()

def generate_env_template():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_file = project_root / '.env'
    env_template_file = project_root / '.env.template'

    if not env_file.exists():
        print(f"{Fore.RED}✗ Error: .env file does not exist.{Style.RESET_ALL}")
        return

    template_lines = [
        "# APP SETUP\n",
        "APP_ENV=\n",
        "APP_DEBUG=\n",
        "APP_PORT=\n",
        "OS_TYPE=\n",
        "\n",
        "# ANTHROPIC SETUP\n",
        "ANTHROPIC_API_KEY=\n",
        "\n",
        "# SUPABASE SETUP\n",
        "SUPABASE_URL=\n",
        "SUPABASE_KEY=\n",
        "SUPABASE_JWT_SECRET=\n",
        "\n",
        "# CORS SETUP\n",
        "CORS_ORIGINS=\n",
    ]

    with open(env_template_file, 'w') as f:
        f.writelines(template_lines)

    relative_path = env_template_file.relative_to(project_root)
    print(f"{Fore.GREEN}✓ .env.template has been generated/updated at ./{relative_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    generate_env_template()