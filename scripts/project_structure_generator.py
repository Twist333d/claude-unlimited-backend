import os
import fnmatch
import argparse
from pathlib import Path


def generate_structure(root_dir, output_file, include_patterns=None, important_patterns=None, exclude_dirs=None):
    if include_patterns is None:
        include_patterns = ['*.js', '*.jsx', '*.ts', '*.tsx', '*.html', '*.css', '*.scss', '*.json', '*.py']
    if important_patterns is None:
        important_patterns = ['README*', 'package.json', 'webpack.config.*', '.gitignore', '.env*', 'Procfile']
    if exclude_dirs is None:
        exclude_dirs = {'node_modules', '.git', '.idea', '__pycache__', 'venv', 'env', '.gitignore'}

    def matches_patterns(file, patterns):
        return any(fnmatch.fnmatch(file, pattern) for pattern in patterns)

    def should_exclude_dir(dir_name):
        return dir_name in exclude_dirs

    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
            level = root.replace(str(root_dir), '').count(os.sep)
            indent = ' ' * 4 * level
            relevant_files = [file for file in files if
                              matches_patterns(file, include_patterns) or matches_patterns(file, important_patterns)]
            if relevant_files or level == 0:  # Always include root directory
                f.write(f'{indent}{os.path.basename(root)}/\n')
                subindent = ' ' * 4 * (level + 1)
                for file in relevant_files:
                    f.write(f'{subindent}{file}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate project structure')
    parser.add_argument('--root', default=None, help='Root directory of the project')
    parser.add_argument('--output', default='project_structure.txt', help='Output file name')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    project_root = script_dir.parent if args.root is None else Path(args.root)
    output_file = project_root / args.output

    generate_structure(project_root, output_file)
    print(f'Project structure has been written to {output_file}')