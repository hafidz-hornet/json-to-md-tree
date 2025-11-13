import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


def extract_const_block(source: str, const_name: str) -> List[str]:
    """
    Extract lines belonging to `const <const_name> = { ... }`
    (without the outer const line and closing `};`).
    """
    lines = source.splitlines()
    in_const = False
    block_lines: List[str] = []

    const_pattern = re.compile(rf"\bconst\s+{re.escape(const_name)}\s*=")

    for line in lines:
        if not in_const:
            if const_pattern.search(line):
                in_const = True
            continue

        # Stop when we hit the end of the object or export default
        if re.match(r"\s*};\s*$", line) or re.search(r"\bexport\s+default\b", line):
            break

        block_lines.append(line)

    if not in_const:
        raise ValueError(f"Could not find `const {const_name} =` in file.")

    if not block_lines:
        raise ValueError(f"No object body found for `const {const_name}`.")

    return block_lines


KeyRecord = Tuple[int, str]  # (indent_spaces, key)


def find_property_keys(block_lines: List[str]) -> List[KeyRecord]:
    """
    Scan the object body and find property keys based on indentation.
    Only looks at lines like:
        key: value
        "key": value
        'key': value
    """
    records: List[KeyRecord] = []

    # Regex for unquoted and quoted keys
    ident_key_re = re.compile(r"^(\s*)([A-Za-z0-9_$]+)\s*:")
    quoted_key_re = re.compile(r"""^(\s*)["']([^"']+)["']\s*:""")

    for line in block_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip obvious comment lines
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        m = ident_key_re.match(line)
        if not m:
            m = quoted_key_re.match(line)

        if not m:
            continue

        indent = len(m.group(1))
        key = m.group(2)
        records.append((indent, key))

    if not records:
        raise ValueError("No property keys found in object body (check formatting).")

    return records


def build_tree_from_keys(const_name: str, records: List[KeyRecord]) -> Dict:
    """
    Build a nested dict tree from (indent, key) records.
    Indentation is assumed to be consistent (e.g. 2 spaces per level).
    """
    tree: Dict[str, Dict] = {const_name: {}}
    root_container = tree[const_name]

    # Determine base indent (top-level keys)
    base_indent = min(indent for indent, _ in records)

    # Guess indentation step: use smallest non-zero difference
    diffs = sorted(
        {indent - base_indent for indent, _ in records if indent - base_indent > 0}
    )
    indent_step = diffs[0] if diffs else 2  # fallback to 2 spaces

    # Stack holds tuples of (level, container_dict)
    # level -1 is the const itself
    stack: List[Tuple[int, Dict]] = [(-1, root_container)]

    for indent, key in records:
        # Compute logical level: 1 = direct child of const
        level = 1 + (indent - base_indent) // indent_step
        if level < 1:
            level = 1

        # Pop to the correct parent level
        while stack and stack[-1][0] >= level:
            stack.pop()

        parent = stack[-1][1]
        # Only create container if not exists
        if key not in parent:
            parent[key] = {}

        # Treat every key as potential parent (even if leaf)
        stack.append((level, parent[key]))

    return tree


def tree_to_md_lines(name: str, subtree: Dict, prefix: str = "", is_last: bool = True) -> List[str]:
    """
    Convert nested dict tree into markdown-style ASCII tree lines.
    """
    lines: List[str] = []
    connector = "└── " if is_last else "├── "
    line = f"{prefix}{connector}{name}" if prefix else name
    lines.append(line)

    # Prepare new prefix for children
    # For root level (no prefix), children should start with no prefix but will get connectors
    # For nested levels, extend the prefix based on whether this is the last child
    child_prefix = prefix + ("    " if is_last else "│   ")

    children = list(subtree.items())
    # Only show children if there are any
    if children:
        for idx, (child_name, child_subtree) in enumerate(children):
            last_child = idx == len(children) - 1
            lines.extend(tree_to_md_lines(child_name, child_subtree, child_prefix, last_child))

    return lines


def convert_ts_const_to_md(path: Path, const_name: str) -> str:
    source = path.read_text(encoding="utf-8")
    block_lines = extract_const_block(source, const_name)
    records = find_property_keys(block_lines)
    tree = build_tree_from_keys(const_name, records)
    
    # There is only one root key: const_name
    root_subtree = tree[const_name]
    lines = tree_to_md_lines(const_name, root_subtree, prefix="", is_last=True)
    return "```text\n" + "\n".join(lines) + "\n```"


def main():
    import sys
    import io
    # Ensure UTF-8 encoding for output (fixes Windows PowerShell encoding issues)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(
        description="Convert a TS/JS const object to markdown folder-style structure."
    )
    parser.add_argument("--file", required=True, help="Path to the TS/JS file")
    parser.add_argument(
        "--const", required=True, dest="const_name", help="Const name to extract (e.g. japanese)"
    )
    parser.add_argument(
        "--output", dest="output_file", help="Optional: Path to output markdown file"
    )
    args = parser.parse_args()

    ts_path = Path(args.file)

    if not ts_path.exists():
        print(f"❌ File not found: {ts_path}")
        return

    try:
        md_output = convert_ts_const_to_md(ts_path, args.const_name)
        
        if args.output_file:
            # Write to file
            output_path = Path(args.output_file)
            output_path.write_text(md_output, encoding="utf-8")
            print(f"✅ Output written to: {output_path}")
        else:
            # Print to stdout
            print(md_output)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
