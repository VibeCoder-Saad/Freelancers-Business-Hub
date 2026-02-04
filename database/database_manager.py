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
    conn.execute("PRAGMA journal_mode = WAL") # Enable Write-Ahead Logging for better concurrency
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
    
    # --- NEW: Monitoring Tables ---
    cursor.execute("CREATE TABLE IF NOT EXISTS activity_logs (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, window_title TEXT, start_time TEXT NOT NULL, end_time TEXT, FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS screenshots (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, file_path TEXT NOT NULL, timestamp TEXT NOT NULL, is_uploaded INTEGER DEFAULT 0, FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS invitations (id INTEGER PRIMARY KEY, project_name TEXT NOT NULL, client_id INTEGER NOT NULL, freelancer_username TEXT NOT NULL, status TEXT DEFAULT 'Pending', rate REAL, created_at TEXT NOT NULL, FOREIGN KEY (client_id) REFERENCES users (id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, sender_id INTEGER NOT NULL, content TEXT NOT NULL, timestamp TEXT NOT NULL, FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE);")
    
    conn.commit()
    conn.close()
    
    # Run migrations for existing databases
    migrate_schema()

def migrate_schema():
    """Updates existing tables with new columns if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'Freelancer'")
        cursor.execute("ALTER TABLE users ADD COLUMN consent_given INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN consent_timestamp TEXT")
    except sqlite3.OperationalError:
        pass # Columns likely exist

    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN freelancer_id INTEGER")
        cursor.execute("ALTER TABLE projects ADD COLUMN is_shared INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Columns likely exist
    conn.commit()
    conn.close()

def user_exists():
    conn = get_db_connection()
    user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    conn.close()
    return user is not None

def create_user(username, password, role="Freelancer", consent_given=0):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, role, consent_given, consent_timestamp) VALUES (?, ?, ?, ?, ?)",
            (username, hashed_password, role, consent_given, datetime.now().isoformat())
        )
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
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return True
    return False

def get_user_role(username):
    conn = get_db_connection()
    user = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user['role'] if user else "Freelancer"

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
def get_dashboard_kpis(user_id=None, role="Freelancer"):
    conn = get_db_connection()
    if role == "Freelancer":
        # Freelancer Logic (assuming they are linked to projects via freelancer_id potentially, but for now let's assume global allowed OR fix schema linkage later)
        # The user requested 'No Garbage', so if a new user comes, they should see 0.
        # Since currently invoices table links to client_id, and projects links to client_id.
        # There is no direct link to freelancer_id in invoices yet explicitly enforced for "My Invoices".
        # However, for this MVP fix, if we want 0 for new user, we must filter.
        # Let's check projects assigned to this freelancer.
        
        # 1. Active Projects (User has to be the freelancer assigned)
        # Note: In `accept_invitation` we set freelancer_id.
        active_projects_data = conn.execute("SELECT COUNT(id) FROM projects WHERE status = 'Active' AND freelancer_id = ?", (user_id,)).fetchone()
        active_projects = active_projects_data[0] if active_projects_data[0] else 0
        
        # 2. Revenue (Invoices linked to projects linked to this freelancer)
        # This requires a JOIN: Invoice -> Project (via time entries?) Or Invoice -> Client.
        # Currently Schema: Invoice -> Client. Time Entry -> Invoice. Time Entry -> Project.
        # So: Invoice <- TimeEntry -> Project -> Freelancer. 
        # Complex JOIN. Let's simplify: Any custom app logic should ideally store 'freelancer_id' on invoice but we don't have it.
        # But we can assume if no projects, then 0 revenue.
        
        # Actually, let's use the `time_entries` link.
        # Sum of invoices where invoice_id is in time_entries of projects owned by freelancer.
        revenue_query = """
            SELECT SUM(i.total_amount) 
            FROM invoices i
            WHERE i.status = 'Paid' 
            AND i.id IN (
                SELECT DISTINCT te.invoice_id 
                FROM time_entries te 
                JOIN projects p ON te.project_id = p.id 
                WHERE p.freelancer_id = ?
            )
        """
        rev_data = conn.execute(revenue_query, (user_id,)).fetchone()
        total_revenue = rev_data[0] if rev_data and rev_data[0] else 0.0

        # 3. Unpaid
        unpaid_query = """
            SELECT SUM(i.total_amount) 
            FROM invoices i
            WHERE i.status IN ('Draft', 'Sent', 'Overdue')
            AND i.id IN (
                SELECT DISTINCT te.invoice_id 
                FROM time_entries te 
                JOIN projects p ON te.project_id = p.id 
                WHERE p.freelancer_id = ?
            )
        """
        unpaid_data = conn.execute(unpaid_query, (user_id,)).fetchone()
        total_unpaid = unpaid_data[0] if unpaid_data and unpaid_data[0] else 0.0

        # 4. Hours
        this_month = datetime.now().strftime('%Y-%m')
        hours_query = """
            SELECT SUM(te.duration_minutes) 
            FROM time_entries te
            JOIN projects p ON te.project_id = p.id
            WHERE p.freelancer_id = ? 
            AND strftime('%Y-%m', te.start_time) = ?
        """
        hours_data = conn.execute(hours_query, (user_id, this_month)).fetchone()
        logged_hours = (hours_data[0] / 60.0) if hours_data and hours_data[0] else 0.0

    else:
        # Client Logic
        # Filter by client_id = user_id (assuming Client User ID maps to Client Table ID or logic handles it)
        # In `accept_invitation`, we query Clients table by Name=Username.
        # So we first need the Client ID from the Clients table, not User table ID.
        client_entry = conn.execute("SELECT id FROM clients WHERE name = (SELECT username FROM users WHERE id = ?)", (user_id,)).fetchone()
        real_client_id = client_entry['id'] if client_entry else -1

        rev_data = conn.execute("SELECT SUM(total_amount) FROM invoices WHERE status = 'Paid' AND client_id = ?", (real_client_id,)).fetchone()
        total_revenue = rev_data[0] if rev_data and rev_data[0] else 0.0 # Actually Expense for client

        unpaid_data = conn.execute("SELECT SUM(total_amount) FROM invoices WHERE status != 'Paid' AND client_id = ?", (real_client_id,)).fetchone()
        total_unpaid = unpaid_data[0] if unpaid_data and unpaid_data[0] else 0.0
        
        active_projects_data = conn.execute("SELECT COUNT(id) FROM projects WHERE status = 'Active' AND client_id = ?", (real_client_id,)).fetchone()
        active_projects = active_projects_data[0] if active_projects_data[0] else 0

        logged_hours = 0.0

    conn.close()
    return {
        "total_revenue": total_revenue, 
        "total_unpaid": total_unpaid, 
        "active_projects": active_projects, 
        "logged_hours_this_month": logged_hours
    }
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

# --- Monitoring Logging ---
def log_activity(project_id, window_title):
    conn = get_db_connection()
    # Simplified: just logging start time as "now"
    conn.execute("INSERT INTO activity_logs (project_id, window_title, start_time) VALUES (?, ?, ?)", 
                 (project_id, window_title, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_screenshot(project_id, file_path):
    conn = get_db_connection()
    conn.execute("INSERT INTO screenshots (project_id, file_path, timestamp) VALUES (?, ?, ?)", 
                 (project_id, file_path, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def update_screenshot_upload_status(file_path, is_uploaded=1):
    conn = get_db_connection()
    conn.execute("UPDATE screenshots SET is_uploaded = ? WHERE file_path = ?", (is_uploaded, file_path))
    conn.commit()
    conn.close()

def get_screenshots_for_project(project_id):
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM screenshots WHERE project_id = ? ORDER BY timestamp DESC", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in data]

def get_activity_logs(project_id):
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM activity_logs WHERE project_id = ? ORDER BY start_time DESC LIMIT 50", (project_id,)).fetchall()
    conn.close()
    return [dict(row) for row in data]

# --- Invitation & Collaborative Project Functions ---

def create_invitation(project_name, client_id, freelancer_username, rate=0.0):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO invitations (project_name, client_id, freelancer_username, status, rate, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (project_name, client_id, freelancer_username, 'Pending', rate, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating invitation: {e}")
        return False
    finally:
        conn.close()

def get_invitations_for_freelancer(username):
    conn = get_db_connection()
    invitations = conn.execute(
        "SELECT i.*, u.username as client_username FROM invitations i JOIN users u ON i.client_id = u.id WHERE i.freelancer_username = ? AND i.status = 'Pending' ORDER BY i.created_at DESC", 
        (username,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in invitations]

def get_user_id_by_username(username):
    conn = get_db_connection()
    user = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user['id'] if user else None

def accept_invitation(invitation_id, freelancer_id):
    conn = get_db_connection()
    try:
        # 1. Get invitation details
        inv = conn.execute("SELECT * FROM invitations WHERE id = ?", (invitation_id,)).fetchone()
        if not inv or inv['status'] != 'Pending':
            return False, "Invitation invalid or not pending"

        # 2. Get client details (to link project correctly) - client is already a 'user' but we treat them as 'client' in projects table?
        # Wait, the current projects table links to 'clients' table, not 'users'.
        # For this simulated environment, we need to ensure the inviting user exists in 'clients' table or change projects schema.
        # The plan said: "Add freelancer_id (FK to users) to track assignment."
        # And "Add is_shared (Boolean)".
        # For simplicity in this demo, we will create a 'Client' record in 'clients' table for the user if it doesn't exist, 
        # or just assume the Demo Client User has a corresponding entry in 'clients'.
        # Let's check if a client with this user's name exists, if not create one.
        
        client_user = conn.execute("SELECT * FROM users WHERE id = ?", (inv['client_id'],)).fetchone()
        client_name = client_user['username']
        
        # Check clients table
        client_entry = conn.execute("SELECT id FROM clients WHERE name = ?", (client_name,)).fetchone()
        if not client_entry:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (client_name, f"{client_name}@example.com"))
            client_db_id = cursor.lastrowid
        else:
            client_db_id = client_entry['id']

        # 3. Create Project
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, client_id, status, rate, freelancer_id, is_shared) VALUES (?, ?, ?, ?, ?, 1)",
            (inv['project_name'], client_db_id, 'Active', inv['rate'], freelancer_id)
        )
        
        # 4. Update Invitation Status
        conn.execute("UPDATE invitations SET status = 'Accepted' WHERE id = ?", (invitation_id,))
        
        conn.commit()
        return True, "Project created successfully"
    except Exception as e:
        print(f"Error accepting invitation: {e}")
        return False, str(e)
    finally:
        conn.close()

# --- Chat Functions ---
def send_message(project_id, sender_id, content):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO messages (project_id, sender_id, content, timestamp) VALUES (?, ?, ?, ?)",
            (project_id, sender_id, content, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False
    finally:
        conn.close()

def get_messages(project_id):
    conn = get_db_connection()
    messages = conn.execute(
        # Join with users to get sender name. 
        # Note: sender_id refers to 'users.id'.
        """
        SELECT m.*, u.username as sender_name 
        FROM messages m 
        JOIN users u ON m.sender_id = u.id 
        WHERE m.project_id = ? 
        ORDER BY m.timestamp ASC
        """, 
        (project_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in messages]

initialize_database()