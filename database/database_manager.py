# database/database_manager.py

import sqlite3
import os
import bcrypt
from datetime import datetime

# --- Database Setup ---
DB_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(DB_DIR, "freelancer_hub.db") # CORRECTED PATH

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# --- The rest of your file is unchanged until the delete section ---
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, address TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT NOT NULL, client_id INTEGER NOT NULL, status TEXT DEFAULT 'Active', rate REAL DEFAULT 0.0, FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS time_entries (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, start_time TEXT NOT NULL, end_time TEXT, duration_minutes INTEGER, description TEXT, is_billed INTEGER DEFAULT 0, invoice_id INTEGER, FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE, FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE SET NULL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, invoice_number TEXT UNIQUE NOT NULL, client_id INTEGER NOT NULL, issue_date TEXT NOT NULL, due_date TEXT NOT NULL, status TEXT DEFAULT 'Draft', total_amount REAL, pdf_path TEXT, FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS invoice_items (id INTEGER PRIMARY KEY, invoice_id INTEGER NOT NULL, description TEXT NOT NULL, quantity REAL NOT NULL, rate REAL NOT NULL, amount REAL NOT NULL, FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, description TEXT NOT NULL, category TEXT, amount REAL NOT NULL, expense_date TEXT NOT NULL, receipt_path TEXT);")
    conn.commit()
    conn.close()

def user_exists():
    conn = get_db_connection()
    user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    conn.close()
    return user is not None

def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError: return False
    finally: conn.close()

def check_user(username, password):
    conn = get_db_connection()
    user = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return True
    return False

def get_all_settings():
    conn = get_db_connection()
    settings = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {row['key']: row['value'] for row in settings}

def save_setting(key, value):
    conn = get_db_connection()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def add_client(name, email, address): conn = get_db_connection(); conn.execute("INSERT INTO clients (name, email, address) VALUES (?, ?, ?)", (name, email, address)); conn.commit(); conn.close()
def get_all_clients(): conn = get_db_connection(); clients = conn.execute("SELECT * FROM clients ORDER BY name ASC").fetchall(); conn.close(); return [dict(row) for row in clients]
def get_client_by_id(client_id): conn = get_db_connection(); client = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone(); conn.close(); return dict(client) if client else None
def add_project(name, client_id, rate): conn = get_db_connection(); conn.execute("INSERT INTO projects (name, client_id, rate) VALUES (?, ?, ?)", (name, client_id, rate)); conn.commit(); conn.close()
def get_all_projects_with_client_name(): conn = get_db_connection(); projects = conn.execute("SELECT p.id, p.name, p.status, p.rate, c.name as client_name, p.client_id FROM projects p JOIN clients c ON p.client_id = c.id ORDER BY p.name ASC").fetchall(); conn.close(); return [dict(row) for row in projects]
def get_project_details(project_id): conn = get_db_connection(); project = conn.execute("SELECT p.id, p.name, p.status, p.rate, c.name as client_name FROM projects p JOIN clients c ON p.client_id = c.id WHERE p.id = ?", (project_id,)).fetchone(); conn.close(); return dict(project) if project else None
def start_time_entry(project_id, start_time): conn = get_db_connection(); cursor = conn.cursor(); cursor.execute("INSERT INTO time_entries (project_id, start_time) VALUES (?, ?)", (project_id, start_time.isoformat())); conn.commit(); entry_id = cursor.lastrowid; conn.close(); return entry_id
def stop_time_entry(entry_id, end_time, duration_minutes, description): conn = get_db_connection(); conn.execute("UPDATE time_entries SET end_time = ?, duration_minutes = ?, description = ? WHERE id = ?", (end_time.isoformat(), duration_minutes, description, entry_id)); conn.commit(); conn.close()
def get_time_entries_for_project(project_id): conn = get_db_connection(); entries = conn.execute("SELECT * FROM time_entries WHERE project_id = ? ORDER BY start_time DESC", (project_id,)).fetchall(); conn.close(); return [dict(row) for row in entries]
def get_unbilled_time_for_project(project_id): conn = get_db_connection(); entries = conn.execute("SELECT * FROM time_entries WHERE project_id = ? AND is_billed = 0 AND duration_minutes IS NOT NULL", (project_id,)).fetchall(); conn.close(); return [dict(row) for row in entries]
def get_next_invoice_number():
    conn = get_db_connection()
    last_inv = conn.execute("SELECT invoice_number FROM invoices ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    if not last_inv:
        return f"INV-{datetime.now().year}-001"
    last_num = int(last_inv['invoice_number'].split('-')[-1])
    return f"INV-{datetime.now().year}-{last_num + 1:03d}"
def create_invoice_from_time_entries(invoice_data, line_items, time_entry_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, status, total_amount) VALUES (?, ?, ?, ?, ?, ?)",
        (invoice_data['invoice_number'], invoice_data['client_id'], invoice_data['issue_date'], invoice_data['due_date'], 'Draft', invoice_data['total_amount'])
    )
    invoice_id = cursor.lastrowid
    for item in line_items:
        cursor.execute(
            "INSERT INTO invoice_items (invoice_id, description, quantity, rate, amount) VALUES (?, ?, ?, ?, ?)",
            (invoice_id, item['description'], item['quantity'], item['rate'], item['amount'])
        )
    if time_entry_ids:
        cursor.execute(
            f"UPDATE time_entries SET is_billed = 1, invoice_id = ? WHERE id IN ({','.join('?' for _ in time_entry_ids)})",
            [invoice_id] + time_entry_ids
        )
    conn.commit()
    conn.close()
    return invoice_id
def update_invoice_pdf_path(invoice_id, pdf_path): conn = get_db_connection(); conn.execute("UPDATE invoices SET pdf_path = ? WHERE id = ?", (pdf_path, invoice_id)); conn.commit(); conn.close()
def get_all_invoices_with_details(): conn = get_db_connection(); invoices = conn.execute("SELECT i.id, i.invoice_number, i.status, i.total_amount, i.issue_date, c.name as client_name FROM invoices i JOIN clients c ON i.client_id = c.id ORDER BY i.id DESC").fetchall(); conn.close(); return [dict(row) for row in invoices]
def get_invoices_for_project(project_id): conn = get_db_connection(); invoices = conn.execute("SELECT DISTINCT i.* FROM invoices i JOIN time_entries te ON i.id = te.invoice_id WHERE te.project_id = ? ORDER BY i.issue_date DESC", (project_id,)).fetchall(); conn.close(); return [dict(row) for row in invoices]
def add_expense(description, category, amount, expense_date, receipt_path=None): conn = get_db_connection(); conn.execute("INSERT INTO expenses (description, category, amount, expense_date, receipt_path) VALUES (?, ?, ?, ?, ?)", (description, category, amount, expense_date, receipt_path)); conn.commit(); conn.close()
def get_all_expenses(): conn = get_db_connection(); expenses = conn.execute("SELECT * FROM expenses ORDER BY expense_date DESC").fetchall(); conn.close(); return [dict(row) for row in expenses]
def get_project_financial_summary(project_id): conn = get_db_connection(); total_hours_data = conn.execute("SELECT SUM(duration_minutes) as total FROM time_entries WHERE project_id = ?", (project_id,)).fetchone(); total_hours = (total_hours_data['total'] / 60.0) if total_hours_data['total'] else 0.0; billed_amount_data = conn.execute("SELECT SUM(ii.amount) as total FROM invoice_items ii JOIN invoices i ON ii.invoice_id = i.id JOIN time_entries te ON i.id = te.invoice_id WHERE te.project_id = ?", (project_id,)).fetchone(); billed_amount = billed_amount_data['total'] if billed_amount_data['total'] else 0.0; conn.close(); return {"total_hours": total_hours, "billed_amount": billed_amount}
def get_dashboard_kpis(): conn = get_db_connection(); total_revenue_data = conn.execute("SELECT SUM(total_amount) FROM invoices WHERE status = 'Paid'").fetchone(); total_revenue = total_revenue_data[0] if total_revenue_data[0] else 0.0; total_unpaid_data = conn.execute("SELECT SUM(total_amount) FROM invoices WHERE status IN ('Draft', 'Sent', 'Overdue')").fetchone(); total_unpaid = total_unpaid_data[0] if total_unpaid_data[0] else 0.0; active_projects_data = conn.execute("SELECT COUNT(id) FROM projects WHERE status = 'Active'").fetchone(); active_projects = active_projects_data[0] if active_projects_data[0] else 0; this_month = datetime.now().strftime('%Y-%m'); logged_hours_data = conn.execute("SELECT SUM(duration_minutes) FROM time_entries WHERE strftime('%Y-%m', start_time) = ?", (this_month,)).fetchone(); logged_hours_this_month = (logged_hours_data[0] / 60.0) if logged_hours_data[0] else 0.0; conn.close(); return {"total_revenue": total_revenue, "total_unpaid": total_unpaid, "active_projects": active_projects, "logged_hours_this_month": logged_hours_this_month}
def get_recent_activity(limit=5): conn = get_db_connection(); activity = conn.execute("SELECT te.start_time, te.duration_minutes, te.description, p.name as project_name FROM time_entries te JOIN projects p ON te.project_id = p.id WHERE te.duration_minutes IS NOT NULL ORDER BY te.start_time DESC LIMIT ?", (limit,)).fetchall(); conn.close(); return [dict(row) for row in activity]
def get_monthly_income_summary(months=6): conn = get_db_connection(); summary = conn.execute("SELECT strftime('%Y-%m', issue_date) as month, SUM(total_amount) as total FROM invoices WHERE status = 'Paid' AND issue_date >= date('now', '-' || ? || ' months') GROUP BY month ORDER BY month ASC", (months,)).fetchall(); conn.close(); return {row['month']: row['total'] for row in summary}

# --- Delete Functions ---
def delete_client(client_id): conn = get_db_connection(); conn.execute("DELETE FROM clients WHERE id = ?", (client_id,)); conn.commit(); conn.close()
def delete_project(project_id): conn = get_db_connection(); conn.execute("DELETE FROM projects WHERE id = ?", (project_id,)); conn.commit(); conn.close()
def delete_invoice(invoice_id): conn = get_db_connection(); conn.execute("UPDATE time_entries SET is_billed = 0, invoice_id = NULL WHERE invoice_id = ?", (invoice_id,)); conn.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,)); conn.commit(); conn.close()
def delete_expense(expense_id): conn = get_db_connection(); conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,)); conn.commit(); conn.close()

# --- NEW: Function to delete a time entry ---
def delete_time_entry(entry_id):
    """Deletes a single time entry record from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM time_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

initialize_database()