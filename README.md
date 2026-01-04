<div align="center">

  <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Logo.png?raw=true" alt="logo" width="200" height="auto" />
  <h1>Freelancer's Business Hub</h1>
  
  <p>
    <b>The All-In-One Offline Command Center for Freelancers</b>
  </p>
  
  <p>
    Manage clients, track time, generate invoices, and analyze revenue—securely and locally.
  </p>


<!-- Badges -->
<p>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python"/>
  </a>
  <a href="https://doc.qt.io/qtforpython/">
    <img src="https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="pyside6"/>
  </a>
  <a href="https://sqlite.org/">
    <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="sqlite"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="license"/>
  </a>
</p>

<br />

<img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Dashboard.PNG?raw=true" alt="Dashboard" width="100%" />

</div>

<br /> 

# 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Visual Showcase](#-visual-showcase)
- [Installation](#-installation)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [License](#-license)

---

# ⚡ Overview

**Freelancer's Business Hub** is a professional desktop application designed to replace scattered spreadsheets and online subscriptions. It offers a **secure, offline-first** environment where you own your data. Whether you are a developer, designer, or consultant, this tool helps you stay on top of your business/

> **Privacy Focused**: No cloud, no tracking, no monthly fees. Your financial data stays on your machine.

---

# 🚀 Key Features

<table>
  <tr>
    <td width="50%">
      <h3>🔐 Secure Local Login</h3>
      <p>Enterprise-grade security on your desktop. Your data is protected by a custom encryption system and a beautiful, animated login screen using <code>bcrypt</code> hashing.</p>
    </td>
    <td width="50%">
      <h3>📊 Analytics Dashboard</h3>
      <p>Make data-driven decisions. Visualize your revenue, active projects, and client growth with real-time, interactive charts powered by <code>Matplotlib</code>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🗂️ Project Command Center</h3>
      <p>A dedicated hub for every project. Track budget usage, view time logs, manage invoices, and store project notes in one unified view.</p>
    </td>
    <td width="50%">
      <h3>⏱️ Precision Time Tracking</h3>
      <p>Never lose a billable minute. The integrated "Start/Stop" timer logs sessions directly to projects, ready for instant invoicing.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>💵 One-Click Invoicing</h3>
      <p>Turn time into money. Generate professional PDF invoices automatically from your time logs. Customize them with your logo and brand colors.</p>
    </td>
    <td width="50%">
      <h3>🧾 Expense Manager</h3>
      <p>Keep your profits clear. Log business expenses, categorize them (Software, Hardware, Travel), and attach digital receipts for tax season.</p>
    </td>
  </tr>
</table>

---

# 🎨 Visual Showcase

<div align="center">

| **Authentication** | **Project Management** |
|:---:|:---:|
| <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/signin.PNG?raw=true" width="400"/> | <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/ProjectHub.PNG?raw=true" width="400"/> |
| **Secure Login** | **Interactive Project Hub** |

| **Time & Money** | **Business Output** |
|:---:|:---:|
| <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/timetracking.PNG?raw=true" width="400"/> | <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Invoices.PNG?raw=true" width="400"/> |
| **Live Time Tracking** | **PDF Invoicing** |

</div>

---

# 💻 Installation

Get up and running in minutes.

### Prerequisites

*   **Python 3.10+** (Recommended)
*   **Git**

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/VibeCoder-Saad/Freelancers-Business-Hub.git
    cd Freelancers-Business-Hub
    ```

2.  **Install Dependencies**
    ```bash
    pip install PySide6 bcrypt fpdf2 matplotlib
    ```

3.  **Launch**
    ```bash
    python main.py
    ```

---

# 🏗️ Technology Stack

This project is built with a focus on performance, native look-and-feel, and maintainability.

| Component | Tech | Description |
| :--- | :--- | :--- |
| **Core** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | The logic and backend backbone. |
| **UI Framework** | ![PySide6](https://img.shields.io/badge/PySide6-41CD52?style=flat-square&logo=qt&logoColor=white) | Official Python bindings for Qt, enabling a fluid, responsive UI. |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Serverless, self-contained, zero-configuration SQL database. |
| **Charts** | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square&logo=python&logoColor=white) | Powerful plotting library for data visualization. |
| **Security** | ![Bcrypt](https://img.shields.io/badge/Bcrypt-black?style=flat-square) | Industry standard for password hashing and security. |
| **Reporting** | ![FPDF2](https://img.shields.io/badge/FPDF2-red?style=flat-square) | Lightweight PDF generation engine. |

---

# 📁 Project Structure

```bash
freelancer_hub/
├── main.py                 # 🚀 Entry Point
├── assets/                 # 🎨 Static Assets (Icons, Images)
├── database/               # 💾 Persistence Layer
│   └── database_manager.py 
├── shared/                 # 🛠️ Utilities
│   └── pdf_generator.py    
└── ui/                     # 🖥️ Presentation Layer
    ├── views/              #    Feature Screens (Dashboard, Projects, etc.)
    ├── widgets/            #    Reusable Components (Charts, Cards)
    ├── login_window.py     
    ├── main_window.py      
    └── styles.py           
```

---

# 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
