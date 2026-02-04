import sys
import os
import time

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database_manager import (create_user, get_user_id_by_username, create_invitation, 
                                     get_invitations_for_freelancer, accept_invitation, get_db_connection)

def run_test():
    print("--- Starting Invitation Logic Test ---")
    
    timestamp = int(time.time())
    client_user = f"client_{timestamp}"
    freelancer_user = f"freelancer_{timestamp}"
    password = "password123"
    
    print(f"Creating users: {client_user}, {freelancer_user}")
    
    # 1. Create Users
    if not create_user(client_user, password, "Client"):
        print("Failed to create client")
        return
    if not create_user(freelancer_user, password, "Freelancer"):
        print("Failed to create freelancer")
        return
        
    client_id = get_user_id_by_username(client_user)
    freelancer_id = get_user_id_by_username(freelancer_user)
    
    print(f"Client ID: {client_id}, Freelancer ID: {freelancer_id}")
    
    # 2. Create Invitation
    project_name = f"Test Project {timestamp}"
    rate = 50.0
    print(f"Creating invitation for project '{project_name}'")
    
    if create_invitation(project_name, client_id, freelancer_user, rate):
        print("Invitation created successfully.")
    else:
        print("Failed to create invitation.")
        return

    # 3. Verify Invitation Exists for Freelancer
    invites = get_invitations_for_freelancer(freelancer_user)
    if not invites:
        print("No invitations found for freelancer!")
        return
    
    print(f"Found {len(invites)} invitation(s). First one: {invites[0]['project_name']}")
    invitation_id = invites[0]['id']
    
    # 4. Accept Invitation
    print(f"Accepting invitation ID: {invitation_id}")
    success, msg = accept_invitation(invitation_id, freelancer_id)
    if success:
        print(f"Invitation accepted: {msg}")
    else:
        print(f"Failed to accept: {msg}")
        return
        
    # 5. Verify Project Created
    conn = get_db_connection()
    project = conn.execute("SELECT * FROM projects WHERE name = ? AND freelancer_id = ?", (project_name, freelancer_id)).fetchone()
    conn.close()
    
    if project:
        print(f"Project verified in DB: ID {project['id']}, Name '{project['name']}', IsShared {project['is_shared']}")
    else:
        print("Project NOT found in DB!")
        return

    print("--- Test Passed Successfully ---")

if __name__ == "__main__":
    run_test()
