import os

def generate_snapshot():
    # Folders to completely ignore
    exclude_dirs = {'.git', 'venv', 'data', '__pycache__', 'logs', 'notebooks', 'node_modules'}
    # File extensions to include in the content dump
    include_extensions = {'.py', '.md', '.sql', '.gitignore', '.env'}
    
    output_file = "project_snapshot.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("--- FULL PROJECT STRUCTURE ---\n")
        
        # 1. Generate the tree structure first
        for root, dirs, files in os.walk('.'):
            # Modifying dirs in-place to skip excluded ones
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f"{sub_indent}{file}\n")
        
        f.write("\n--- DETAILED FILE CONTENTS ---\n")
        
        # 2. Dump the content of the code files
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in include_extensions):
                    file_path = os.path.join(root, file)
                    f.write(f"\n\nFILE: {file_path}\n")
                    f.write("-" * 30 + "\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as code_file:
                            f.write(code_file.read())
                    except Exception as e:
                        f.write(f"Error reading file: {e}\n")
                    f.write("\n" + "-" * 30 + "\n")

    print(f"✅ Success! Deep snapshot saved to: {output_file}")

if __name__ == "__main__":
    generate_snapshot()