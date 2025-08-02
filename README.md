#  freelancers-business-hub

<p align="center">
  <img src="https://i.ibb.co/jPDmpxZ/briefcase.png" alt="App Logo"/>
</p>

<h1 align="center">Freelancer's Business Hub</h1>

<p align="center">
  A modern, professional, and fully standalone desktop application built with Python and PySide6 to empower freelancers. Manage your entire business workflow—from clients and projects to time tracking and invoicing—in one secure, private, and offline-first application.
</p>

<p align="center">
  <img src="https://i.ibb.co/ymBgByJ/dashboard.png" alt="Application Dashboard Screenshot"/>
</p>

---

## ✨ Core Features

This application transforms your desktop into a complete command center for your freelance business.

*   🔐 **Secure Local Login:** Your data is protected by a secure, local user account system using password hashing (`bcrypt`).
*   📊 **Analytics Dashboard:** Get an instant, at-a-glance overview of your business's financial health with live-updating KPIs and charts for revenue and activity.
*   🗂️ **The Project Hub:** A powerful, interactive command center providing a 360-degree view of any selected project, including its financials, time logs, and associated invoices.
*   ⏱️ **Live Time Tracking:** An integrated "Start/Stop" timer to accurately log every billable minute against specific projects.
*   💵 **Automated Invoicing:** Generate professional, clean PDF invoices from your logged time entries with a single click, complete with your company logo.
*   🧾 **Expense Tracking:** Meticulously log all business costs, categorize them, and attach digital receipts for perfect record-keeping.
*   👥 **Client Management:** A simple yet effective CRM to keep track of all your clients and their contact information.
*   ⚙️ **Data Management:** Customize your company profile, upload your logo, and easily back up or restore your entire business database.
*   🎨 **Modern, Responsive UI:** A beautiful, responsive, and colorful user interface built with modern design principles, complete with a full icon set for intuitive navigation.
*   🔒 **100% Standalone & Private:** No cloud services, no monthly fees, no internet required. All your sensitive client and financial data is stored securely on your local machine.

---

## 🛠️ Tech Stack

*   **GUI Framework:** [PySide6](https://www.qt.io/qt-for-python) (The official Qt for Python bindings)
*   **Database:** [SQLite 3](https://www.sqlite.org/index.html) (via Python's built-in `sqlite3` module)
*   **Charting / Analytics:** [Matplotlib](https://matplotlib.org/)
*   **PDF Generation:** [fpdf2](https://github.com/PyFPDF/fpdf2)
*   **Password Security:** [bcrypt](https://pypi.org/project/bcrypt/)

---

## 🚀 Getting Started

Follow these instructions to get the application running on your local machine.

### Prerequisites

1.  **Python:** You must have Python 3.7 or newer installed. You can download it from [python.org](https://www.python.org/).
    > **Important:** During installation on Windows, make sure to check the box that says **"Add Python to PATH"**.

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

Once the setup is complete, you can start the application with a single command from the root project directory:

```bash
python main.py

On the first run, you will be prompted to create a primary admin account. After that, the beautiful login screen will appear every time you launch the app.
🖼️ Gallery
<table>
<tr>
<td align="center"><b>Modern Login Screen</b></td>
<td align="center"><b>Interactive Project Hub</b></td>
</tr>
<tr>
<td><img src="https://i.ibb.co/BH7TqD9/login.png" alt="Login Screen" width="400"/></td>
<td><img src="https://i.ibb.co/VccmYsb/projecthub.png" alt="Project Hub" width="400"/></td>
</tr>
<tr>
<td align="center"><b>Time Tracking</b></td>
<td align="center"><b>Invoicing & Billing</b></td>
</tr>
<tr>
<td><img src="https://i.ibb.co/wNN1rTk/timetracking.png" alt="Time Tracking" width="400"/></td>
<td><img src="https://i.ibb.co/C5DyGhvx/invoices.png" alt="Invoices" width="400"/></td>
</tr>
<tr>
<td align="center"><b>Client Management</b></td>
<td align="center"><b>Settings & Data Backup</b></td>
</tr>
<tr>
<td><img src="https://i.ibb.co/GGqf283/clients.png" alt="Clients" width="400"/></td>
<td><img src="https://i.ibb.co/HTdGgvB/settings.png" alt="Settings" width="400"/></td>
</tr>
</table>
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
