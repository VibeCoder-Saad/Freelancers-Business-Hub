#  Freelancer's Business Hub

<p align="center">
  <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Logo.png?raw=true" alt="App Logo" width="128"/>
</p>

<h1 align="center">Freelancer's Business Hub</h1>

<p align="center">
  A modern, professional, and fully standalone desktop application built with Python and PySide6 to empower freelancers. Manage your entire business workflow—from clients and projects to time tracking and invoicing—in one secure, private, and offline-first application.
</p>

<p align="center">
  <img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Dashboard.PNG?raw=true" alt="Application Dashboard Screenshot"/>
</p>

---

## ✨ Core Features

This application transforms your desktop into a complete command center for your freelance business.

*   🔐 **Secure Local Login:** Your data is protected by a beautiful, animated login screen and a secure, local user account system using password hashing (`bcrypt`).
*   📊 **Analytics Dashboard:** Get an instant, at-a-glance overview of your business's financial health with live-updating KPIs and charts for revenue and activity.
*   🗂️ **The Project Hub:** A powerful, interactive command center providing a 360-degree view of any selected project, including its financials, time logs, and associated invoices.
*   ⏱️ **Live Time Tracking:** An integrated "Start/Stop" timer to accurately log every billable minute against specific projects.
*   💵 **Automated Invoicing:** Generate professional, clean PDF invoices from your logged time entries with a single click, complete with your custom company logo.
*   🧾 **Expense Tracking:** Meticulously log all business costs, categorize them, and attach digital receipts for perfect record-keeping.
*   👥 **Client Management:** A simple yet effective CRM to keep track of all your clients and their contact information.
*   ⚙️ **Settings & Data Management:** Customize your company profile, upload your logo, and easily back up or restore your entire business database with a single click.
*   🎨 **Modern, Responsive UI:** A beautiful, responsive, and colorful user interface built with modern design principles, complete with a full icon set for intuitive navigation.
*   🔒 **100% Standalone & Private:** No cloud services, no monthly fees, no internet required. All your sensitive client and financial data is stored securely on your local machine.

---

## 🖼️ Gallery

<table>
  <tr>
    <td align="center"><b>Stunning Animated Login</b></td>
    <td align="center"><b>Interactive Project Hub</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/signin.PNG?raw=true" alt="Login Screen" width="400"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/ProjectHub.PNG?raw=true" alt="Project Hub" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>Live Time Tracking</b></td>
    <td align="center"><b>Automated Invoicing</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/timetracking.PNG?raw=true" alt="Time Tracking" width="400"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/Invoices.PNG?raw=true" alt="Invoices" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>Client Management</b></td>
    <td align="center"><b>Settings & Data Backup</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/clients.PNG?raw=true" alt="Clients" width="400"/></td>
    <td><img src="https://github.com/VibeCoder-Saad/Freelancers-Business-Hub/blob/main/assets/docs/settings.PNG?raw=true" alt="Settings" width="400"/></td>
  </tr>
</table>

---

## 🛠️ Tech Stack

*   **GUI Framework:** [PySide6](https://www.qt.io/qt-for-python)
*   **Database:** [SQLite 3](https://www.sqlite.org/index.html) (via Python's built-in `sqlite3` module)
*   **Charting / Analytics:** [Matplotlib](https://matplotlib.org/)
*   **PDF Generation:** [fpdf2](https://github.com/PyFPDF/fpdf2)
*   **Password Security:** [bcrypt](https://pypi.org/project/bcrypt/)

---

## 🚀 Getting Started

Follow these instructions to get the application running on your local machine.

### Prerequisites

1.  **Python:** Python 3.7 or newer is required. Download from [python.org](https://www.python.org/).
    > **Important:** During installation on Windows, ensure you check the box that says **"Add Python to PATH"**.

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/VibeCoder-Saad/Freelancers-Business-Hub.git
    cd Freelancers-Business-Hub
    ```

2.  **Install Dependencies:**
    Open your terminal in the project's root directory and run the following command:
    ```bash
    pip install PySide6 bcrypt fpdf2 matplotlib
    ```

### Running the Application

Start the application with a single command from the root project directory:

```bash
python main.py

On the first run, you will be prompted to create a primary admin account. After that, the login screen will appear every time you launch the app.
📁 Project Structure
freelancer_hub/
│
├── main.py                 # The Application Launcher
├── assets/                 # Icons, backgrounds, and documentation images
├── database/
│   └── database_manager.py # Manages all SQLite database operations
├── shared/
│   └── pdf_generator.py    # Utility for creating invoice PDFs
└── ui/
    ├── login_window.py     # Secure login and registration screen
    ├── main_window.py      # The main application container with all tabs
    ├── styles.py           # The application-wide QSS stylesheet
    ├── views/              # Each feature's UI is a separate "view"
    └── widgets/            # Reusable custom UI components like charts
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
