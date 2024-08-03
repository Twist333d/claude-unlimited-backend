import os
from pathlib import Path

def generate_env_template():
    # Define the paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Assuming scripts is directly under project root
    env_file = project_root / '.env'
    env_template_file = project_root / '.env.template'

    # Check if .env file exists
    if not env_file.exists():
        print(f"Error: {env_file} does not exist.")
        return

    # Read the .env file
    with open(env_file, 'r') as f:
        env_contents = f.readlines()

    # Process each line
    template_lines = []
    for line in env_contents:
        line = line.strip()
        if line and not line.startswith('#'):
            # Split the line into key and value
            key, value = line.split('=', 1)
            # Add the key with an empty value to the template
            template_lines.append(f"{key}=\n")

    # Write the .env.template file
    with open(env_template_file, 'w') as f:
        f.writelines(template_lines)

    print(f".env.template has been generated/updated at {env_template_file}")

if __name__ == "__main__":
    generate_env_template()