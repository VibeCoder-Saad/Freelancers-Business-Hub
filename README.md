# Freelancer's Business Hub

<div align="center">
  <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Logo.png?raw=true" alt="App Logo" width="160"/>
  <br><br>

  [![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/GUI-PySide6-green?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
  [![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)
  [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/VibeCoder-Saad/Freelancers-Business-Hub)

  <h1>Manage Your Business logic Offline & Securely</h1>

  <p>
    <b>Freelancer's Business Hub</b> is a modern, professional, and fully standalone desktop application built to empower freelancers. <br>
    Manage clients, projects, time tracking, and invoicing in one secure, private, and offline-first environment.
  </p>

  <br>
  
  <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Dashboard.PNG?raw=true" alt="Application Dashboard Screenshot" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);"/>
</div>

---

## 📑 Table of Contents

- [✨ Core Features](#-core-features)
- [🖼️ Gallery](#-gallery)
- [🛠️ Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [📁 Project Structure](#-project-structure)
- [📄 License](#-license)

---

## ✨ Core Features

This application transforms your desktop into a complete command center for your freelance business.

| Feature | Description |
| :--- | :--- |
| **🔐 Secure Local Login** | Your data is protected by a beautiful, animated login screen and a secure, local user account system using password hashing (`bcrypt`). |
| **📊 Analytics Dashboard** | Get an instant, at-a-glance overview of your business's financial health with live-updating KPIs and charts for revenue and activity. |
| **🗂️ The Project Hub** | A powerful, interactive command center providing a 360-degree view of any selected project, including its financials, time logs, and invoices. |
| **⏱️ Live Time Tracking** | An integrated "Start/Stop" timer to accurately log every billable minute against specific projects. |
| **💵 Automated Invoicing** | Generate professional, clean PDF invoices from your logged time entries with a single click, complete with your custom company logo. |
| **🧾 Expense Tracking** | Meticulously log all business costs, categorize them, and attach digital receipts for perfect record-keeping. |
| **👥 Client Management** | A simple yet effective CRM to keep track of all your clients and their contact information. |
| **⚙️ Settings & Backup** | Customize your company profile, upload your logo, and easily back up or restore your entire business database with a single click. |
| **🎨 Modern UI** | A beautiful, responsive, and colorful user interface built with modern design principles and a dark theme. |
| **🔒 100% Private** | **No cloud services, no monthly fees, no internet required.** All your sensitive data is stored securely on your local machine. |

---

## 🖼️ Gallery

Explore the beautiful interface designed for productivity.

<div align="center">
<table>
  <tr>
    <td align="center"><b>Stunning Animated Login</b></td>
    <td align="center"><b>Interactive Project Hub</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/signin.PNG?raw=true" alt="Login Screen" width="100%"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/ProjectHub.PNG?raw=true" alt="Project Hub" width="100%"/></td>
  </tr>
  <tr>
    <td align="center"><b>Live Time Tracking</b></td>
    <td align="center"><b>Automated Invoicing</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/timetracking.PNG?raw=true" alt="Time Tracking" width="100%"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Invoices.PNG?raw=true" alt="Invoices" width="100%"/></td>
  </tr>
  <tr>
    <td align="center"><b>Client Management</b></td>
    <td align="center"><b>Settings & Data Backup</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Clients.PNG?raw=true" alt="Clients" width="100%"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Settings.PNG?raw=true" alt="Settings" width="100%"/></td>
  </tr>
</table>
</div>

---

## 🛠️ Tech Stack

Built with robust and efficient technologies.

*   **GUI Framework:** [PySide6](https://www.qt.io/qt-for-python) - The official Python binding for the Qt framework.
*   **Database:** [SQLite 3](https://www.sqlite.org/index.html) - Robust, serverless, and self-contained database engine.
*   **Visualization:** [Matplotlib](https://matplotlib.org/) - For generating dynamic revenue and activity charts.
*   **Reporting:** [fpdf2](https://github.com/PyFPDF/fpdf2) - Simple and effective PDF generation for invoices.
*   **Security:** [bcrypt](https://pypi.org/project/bcrypt/) - Industry-standard password hashing for securing user credentials.

---

## 🚀 Getting Started

Follow these instructions to get the application running on your local machine.

### Prerequisites

*   **Python 3.7+**: Download from [python.org](https://www.python.org/).
    > ⚠️ **Important:** During installation on Windows, ensure you check the box **"Add Python to PATH"**.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/VibeCoder-Saad/Freelancers-Business-Hub.git
    cd Freelancers-Business-Hub
    ```

2.  **Install Dependencies**
    ```bash
    pip install PySide6 bcrypt fpdf2 matplotlib
    ```

3.  **Run the Application**
    ```bash
    python main.py
    ```

> On the first run, you will be prompted to create a primary admin account.

---

## 📁 Project Structure

```bash
freelancer_hub/
├── main.py                 # 🚀 The Application Launcher
├── assets/                 # 🎨 Icons, backgrounds, and images
├── database/
│   └── database_manager.py # 🗄️ Database operations & schema
├── shared/
│   └── pdf_generator.py    # 📄 PDF Invoice generation logic
└── ui/                     # 🖥️ User Interface Implementation
    ├── login_window.py     #    - Secure login/register screen
    ├── main_window.py      #    - Main application container
    ├── styles.py           #    - CSS/QSS Stylesheet
    ├── views/              #    - Individual feature views (Dashboard, Projects, etc.)
    └── widgets/            #    - Reusable UI widgets
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
