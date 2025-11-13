# JSON → Markdown Tree Converter

A simple Python CLI tool that converts a JSON file into a **folder-style markdown tree structure**.

---

## 🚀 Features

- Converts any JSON into a readable markdown folder tree
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

```sh
python app.py --file yourfile.json
```

Example:

```sh
python app.py --file japanese.json
```

Output:

```text
root
├── swal
│   ├── languageSelection
│   └── ...
```

---

## 📁 Project Structure

```
project/
├── app.py
├── README.md
├── .gitignore
└── your.json
```

---

## 🛠 How it works

The script:

1. Loads the JSON
2. Recursively traverses objects/arrays
3. Prints a markdown tree inside a code block


---

## 📜 License

MIT

