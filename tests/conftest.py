import pytest
import sqlite3
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database_manager import initialize_database, get_db_connection

@pytest.fixture
def mock_db(monkeypatch):
    """
    Creates an in-memory database for testing.
    Patches get_db_connection in database_manager to return this connection.
    """
    # Create in-memory DB
    conn = sqlite3.connect(":memory:")
    
    # Initialize Schema
    # We need to manually run the schema creation from database_manager manually 
    # OR monkeypatch the connection used inside initialize_database
    
    # Let's read the schema creation logic from database manager? 
    # Actually, simpler: just use a unique test.db file and delete it after
    test_db_path = "test_database.db"
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        
    def mock_get_conn():
        conn = sqlite3.connect(test_db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    monkeypatch.setattr("database.database_manager.get_db_connection", mock_get_conn)
    
    # Initialize it
    initialize_database()
    
    yield
    
    # Cleanup
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except:
            pass
