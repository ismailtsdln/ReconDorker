<p align="center">
  <img src="https://raw.githubusercontent.com/ismailtsdln/ReconDorker/main/assets/logo.png" width="200" alt="ReconDorker Logo">
</p>

# ReconDorker Pro — Advanced OSINT Intelligence Platform

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Rich](https://img.shields.io/badge/Rich-CLI-green.svg)](https://github.com/Textualize/rich)

**ReconDorker Pro** is an elite, high-performance OSINT reconnaissance framework designed for deep intelligence gathering. By orchestrating advanced dorking techniques across multiple search engines, it automates the discovery of sensitive data, exposed assets, and shadow infrastructure.

---

## ⚡ Key Intelligence Features

- **🛡️ Multi-Engine Discovery**: Leverages **Google**, **Bing**, and **DuckDuckGo** for maximum target coverage.
- **🔍 Recursive Subdomain Hunting**: Automatically identifies and performs deep discovery on nested subdomains.
- **📄 Document Metadata Extraction**: High-fidelity extraction of author, timestamps, and software details from discovered **PDF** and **DOCX** files.
- **📂 Elite Dork Library**: Curated categories for `.env` leaks, SQL dumps, admin panels, and private keys.
- **🎨 Premium Visual Experience**:
  - **CLI**: Immersive real-time progress bars, structured panels, and beautiful colorization powered by `Rich`.
  - **Web Dashboard**: Modern **Glassmorphism** interface with real-time status polling and interactive results.
  - **Reports**: Professional, interactive HTML reports built with **Tailwind CSS**.
- **🔒 Enterprise Reliability**: Integrated **Proxy Rotation** support and adaptive rate-limiting to bypass detection.

---

## 🚀 Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ismailtsdln/ReconDorker.git
   cd ReconDorker
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install production dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

---

## 💻 Professional Usage

### 🛠️ Command Line Interface (CLI)

Perform a comprehensive, recursive scan with multi-engine support:

```bash
python3 -m recondorker.cli -t target.com --category leaks --recursive --engines google --engines bing --open
```

**Advanced Options:**
- `-t, --target`: Target domain (required)
- `-r, --recursive`: Recursively scan discovered subdomains.
- `-e, --engines`: engines to use (`google`, `bing`, `duckduckgo`).
- `-c, --category`: Specific dork categories (e.g., `leaks`, `admin_panels`).
- `--proxy-file`: Path to a list of proxies for rotation.
- `--open`: Automatically open the HTML report after completion.

### 🌐 Web Intelligence Dashboard

Launch the premium FastAPI-powered dashboard:

```bash
uvicorn webui.main:app --host 0.0.0.0 --port 8000
```
Access the dashboard at `http://localhost:8000`.

---

## 📊 Sample Intelligence Report

The generated HTML reports feature:
- Clean, searchable interface.
- Categorized findings with source attribution.
- **Embedded Metadata**: View document properties directly within the report.
- Responsive design for mobile intelligence review.

---

## 🛡️ Ethics & Disclaimer

This software is for educational and authorized security auditing purposes only. Use of ReconDorker against targets without prior written consent is illegal. The developers assume no liability for misuse of this tool.

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---
<p align="center">
  Developed with ❤️ by OSINT Enthusiasts
</p>
