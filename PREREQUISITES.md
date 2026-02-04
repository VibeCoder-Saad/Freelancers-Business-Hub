# System Prerequisites & Installation Guide

Welcome to the **Freelancer's Business Hub**.
This application uses modern Python libraries for GUI (PySide6) and Real-Time features (FastAPI, WebSockets).

## 1. System Requirements

*   **Operating System**: Windows 10/11, macOS (10.15+), or Linux (Ubuntu 20.04+).
    *   *Note: Real-time Window Tracking is currently optimized for Windows.*
*   **Disk Space**: ~200MB free space.
*   **RAM**: 4GB minimum (8GB recommended).

## 2. Software Requirements

### Python
You must have **Python 3.10** or newer installed.
*   Check version: `python --version`
*   Download: [python.org/downloads](https://www.python.org/downloads/)
*   **Important**: During installation, check the box **"Add Python to PATH"**.

## 3. Installation Steps

### Step A: Clone or Download
1.  Download the repository to your local machine.
2.  Open a terminal (Command Prompt or PowerShell) inside the `Freelancers-Business-Hub` folder.

### Step B: Create a Virtual Environment (Recommended)
This keeps your system clean.
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```
*(On macOS/Linux: `source .venv/bin/activate`)*

### Step C: Install Dependencies
Run the following command to install all necessary libraries (`PySide6`, `FastAPI`, `PyAutoGUI`, etc.):
```bash
pip install -r requirements.txt
```

### Step D: Database Initialization
The application automatically creates the database file (`database/freelancer_hub.db`) on the first run. No manual SQL setup is required.

## 4. How to Run

### Desktop App (Freelancer/Client View)
```bash
python main.py
```

### Sync Server (Optional - For Multi-Device Sync)
If you are developing the backend features:
```bash
uvicorn server.main:app --reload
```
