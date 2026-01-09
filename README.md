# ReconDorker — OSINT & Google Dorking Tool

ReconDorker is a powerful Python-based reconnaissance tool that automates Google Hacking (Google Dorking) queries against a target domain. It extracts sensitive information, indexes of directories, and exposed files to help pentester’s and OSINT experts.

## 🚀 Features

- **Automated GHDB Queries**: Parallel execution of Google Dork queries.
- **Advanced Parsing**: Extracts links, titles, and snippets from search results.
- **Reporting**: Generates professional reports in **JSON**, **CSV**, and **HTML**.
- **CLI & Web UI**: Offers both a command-line interface and a modern Web dashboard.
- **Ethical & Configurable**: Supports rate limiting, custom dorks, and proxies.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ismailtsdln/ReconDorker.git
   cd ReconDorker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## 💻 Usage

### CLI

Run a basic scan against a domain:
```bash
recondorker -t example.com -f html -o example_report
```

Options:
- `-t, --target`: Target domain (required)
- `-p, --pages`: Number of pages (default: 1)
- `-f, --format`: Output format (json, csv, html)
- `-o, --output`: Output filename
- `--proxy`: HTTP/S proxy URL

### Web UI

Start the FastAPI server:
```bash
uvicorn webui.main:app --reload
```
Then open `http://127.0.0.1:8000` in your browser.

## 🛡️ Ethics & Disclaimer

This tool is for educational and authorized security testing purposes only. Use it responsibly and legally.

## 📄 License
MIT License
