import os

# Các folder cần bỏ qua
IGNORE_DIRS = {'.venv', '.idea', '.git', '__pycache__','libraries'}
MAX_DEPTH = 30

def count_lines(root_path, depth=0):
    if depth > MAX_DEPTH:
        return 0

    total_lines = 0

    try:
        for entry in os.scandir(root_path):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in IGNORE_DIRS:
                    continue
                print(entry.name)
                total_lines += count_lines(entry.path, depth + 1)
            elif entry.is_file() and entry.name.endswith('.py'):
                try:
                    with open(entry.path, 'r', encoding='utf-8') as f:
                        lines = sum(1 for _ in f)
                        total_lines += lines
                except Exception as e:
                    print(f"⚠️  Lỗi đọc file {entry.path}: {e}")
    except Exception as e:
        print(f"⚠️  Lỗi đọc folder {root_path}: {e}")

    return total_lines

if __name__ == "__main__":
    project_path = os.path.abspath(".")
    total = count_lines(project_path)
    print(f"📄 Tổng số dòng Python trong project: {total}")
