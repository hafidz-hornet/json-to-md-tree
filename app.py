import json
import argparse
from pathlib import Path


def build_tree(data, indent=0):
    """Recursively converts JSON structure into tree-like text."""
    lines = []
    prefix = "│   " * (indent - 1) + ("├── " if indent > 0 else "")

    if isinstance(data, dict):
        for i, (key, value) in enumerate(data.items()):
            is_last = i == len(data) - 1
            connector = "└── " if is_last else "├── "

            if indent == 0:
                lines.append(f"{key}")
            else:
                lines.append(f"{'│   ' * (indent - 1)}{connector}{key}")

            if isinstance(value, (dict, list)):
                lines.extend(build_tree(value, indent + 1))

            else:
                # leaf values
                lines.append(f"{'│   ' * indent}└── value")

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            is_last = idx == len(data) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{'│   ' * (indent - 1)}{connector}[{idx}]")

            if isinstance(item, (dict, list)):
                lines.extend(build_tree(item, indent + 1))

            else:
                lines.append(f"{'│   ' * indent}└── value")

    return lines


def convert_json_to_md(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tree_lines = build_tree(data)
    return "```text\n" + "\n".join(tree_lines) + "\n```"


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to markdown tree")
    parser.add_argument("--file", required=True, help="Path to the JSON file")

    args = parser.parse_args()
    json_path = Path(args.file)

    if not json_path.exists():
        print(f"❌ File not found: {json_path}")
        return

    md_output = convert_json_to_md(json_path)
    print(md_output)


if __name__ == "__main__":
    main()
