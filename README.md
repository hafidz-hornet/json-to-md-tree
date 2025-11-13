# JSON/TS → Markdown Tree Converter

A simple Python CLI tool that converts JSON files or TypeScript/JavaScript const objects into a **folder-style markdown tree structure**.

---

## 🚀 Features

- Converts any JSON into a readable markdown folder tree
- Extracts and converts TypeScript/JavaScript const objects
- Supports nested objects and arrays
- Works via CLI
- Very simple to extend
- Python 3.x compatible

---

## 📦 Installation

```sh
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt # (if you add dependencies)
````

---

## ▶️ Usage

### For JSON files:

```sh
python app.py --file yourfile.json
```

Example:

```sh
python app.py --file test_data.json
```

### For TypeScript/JavaScript const objects:

```sh
python app2.py --file data.ts --const <const_name>
```

Example:

```sh
python app2.py --file japanese_data.ts --const japanese
```

**With output file:**

```sh
python app2.py --file japanese_data.ts --const japanese --output output.md
```

Output:

```text
japanese
├── swal
│   ├── languageSelection
│   │   ├── successTitle
│   │   └── successMessage
│   └── ...
```

---

## 📁 Project Structure

```
project/
├── app.py           # JSON converter
├── app2.py          # TypeScript/JavaScript const converter
├── README.md
├── .gitignore
└── your.json / data.ts
```

> **Note:** Files matching `*data.json` are excluded from version control (see `.gitignore`).

---

## 🛠 How it works

**app.py** (JSON converter):
1. Loads the JSON file
2. Recursively traverses objects/arrays
3. Prints a markdown tree inside a code block

**app2.py** (TS/JS const converter):
1. Extracts the specified const object from the source file
2. Parses property keys based on indentation
3. Builds a nested tree structure
4. Prints a markdown tree inside a code block


---

## 📜 License

MIT

