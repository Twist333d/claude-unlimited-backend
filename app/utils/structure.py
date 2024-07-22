import os
import fnmatch
import argparse


def generate_structure(root_dir, output_file, include_patterns=None, important_patterns=None, exclude_dirs=None):
    if include_patterns is None:
        include_patterns = ['*.js', '*.jsx', '*.ts', '*.tsx', '*.html', '*.css', '*.scss', '*.json', '*.py', '*.md']
    if important_patterns is None:
        important_patterns = ['README*', 'package.json', 'webpack.config.*', '.gitignore', '.env*', 'Procfile',
                              'requirements.txt']
    if exclude_dirs is None:
        exclude_dirs = {'node_modules', '.git', '.idea', '__pycache__', 'venv', 'env'}

    def matches_patterns(file, patterns):
        return any(fnmatch.fnmatch(file, pattern) for pattern in patterns)

    def should_exclude_dir(dir_name):
        return any(excluded in dir_name for excluded in exclude_dirs)

    def get_file_info(file_path):
        try:
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                return first_line if first_line else "Empty file"
        except Exception:
            return "Unable to read file"

    try:
        with open(output_file, 'w') as f:
            for root, dirs, files in os.walk(root_dir):
                dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
                level = root.replace(root_dir, '').count(os.sep)
                indent = '  ' * level
                f.write(f"{indent}{os.path.basename(root)}/\n")
                subindent = '  ' * (level + 1)

                for file in sorted(files):
                    if matches_patterns(file, include_patterns) or matches_patterns(file, important_patterns):
                        file_path = os.path.join(root, file)
                        file_info = get_file_info(file_path)
                        f.write(f"{subindent}{file} - {file_info}\n")

                f.write('\n')  # Add a newline between directories for readability

        print(f"Detailed project structure has been written to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate detailed project structure")
    parser.add_argument('--root', default='.', help="Root directory of the project")
    parser.add_argument('--output', default='./detailed_project_structure.txt', help="Output file path")
    args = parser.parse_args()

    generate_structure(args.root, args.output)