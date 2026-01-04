# controllers/project_controller.py

from datetime import timedelta, datetime
from database.database_manager import (
    get_all_projects_with_client_name,
    get_project_details,
    get_project_financial_summary,
    get_time_entries_for_project,
    get_invoices_for_project,
    add_project,
    delete_project,
    get_all_clients
)

class ProjectController:
    """
    Handles business logic for the Project Hub.
    Interacts with the DatabaseManager and formats data for the View.
    """

    def get_all_projects(self):
        """Returns a list of all projects with client names."""
        return get_all_projects_with_client_name()

    def get_all_clients(self):
        """Returns a list of all clients."""
        return get_all_clients()

    def create_project(self, name, client_id, rate):
        """Creates a new project."""
        return add_project(name, client_id, rate)

    def delete_project(self, project_id):
        """Deletes a project by ID."""
        return delete_project(project_id)

    def get_project_dashboard_data(self, project_id):
        """
        Fetches and aggregates all data needed for the Project Dashboard.
        Returns a dictionary or None if project not found.
        """
        details = get_project_details(project_id)
        if not details:
            return None

        financials = get_project_financial_summary(project_id)
        time_entries = get_time_entries_for_project(project_id)
        invoices = get_invoices_for_project(project_id)

        # Process Time Entries (Format Duration)
        formatted_time_entries = []
        for entry in time_entries:
            duration_minutes = entry.get('duration_minutes')
            if duration_minutes is None:
                duration_text = "Running..."
            else:
                duration_text = str(timedelta(minutes=duration_minutes))
            
            # Format Date
            try:
                date_obj = datetime.fromisoformat(entry['start_time'])
                date_str = date_obj.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                date_str = entry['start_time'] # Fallback

            formatted_time_entries.append({
                "date": date_str,
                "duration": duration_text,
                "description": entry.get('description', '')
            })

        # Process Invoices (Format Amount)
        formatted_invoices = []
        for inv in invoices:
            formatted_invoices.append({
                "number": inv['invoice_number'],
                "date": inv['issue_date'],
                "status": inv['status'],
                "amount": f"${inv['total_amount']:.2f}"
            })

        return {
            "details": details,
            "financials": {
                "total_hours": f"{financials['total_hours']:.2f} hrs",
                "billed_amount": f"${financials['billed_amount']:.2f}"
            },
            "time_entries": formatted_time_entries,
            "invoices": formatted_invoices
        }
