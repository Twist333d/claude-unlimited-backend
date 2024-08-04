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

    with open(env_file, 'r') as f:
        env_contents = f.readlines()

    template_lines = []
    current_section = None
    for line in env_contents:
        line = line.strip()
        if line.startswith('#'):
            if line.startswith('# ') and line.endswith(':'):
                current_section = line
                template_lines.append(f"\n{line}\n")
            else:
                template_lines.append(f"{line}\n")
        elif line:
            key, value = line.split('=', 1)
            comment = f"# {current_section[2:-1]} variable" if current_section else ""
            template_lines.append(f"{key}= {comment}\n")

    with open(env_template_file, 'w') as f:
        f.writelines(template_lines)

    relative_path = env_template_file.relative_to(project_root)
    print(f"{Fore.GREEN}✓ .env.template has been generated/updated at ./{relative_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    generate_env_template()