from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Database schema setup functions
def create_tables():
    """
    Create necessary tables in Supabase if they don't exist.
    Run this once to set up your database schema.
    """
    
    # Users table
    users_schema = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        location VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # Predictions table
    predictions_schema = """
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100) NOT NULL,
        severity FLOAT NOT NULL,
        prediction_data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # Alerts table
    alerts_schema = """
    CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        message TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # Resources table
    resources_schema = """
    CREATE TABLE IF NOT EXISTS resources (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100) NOT NULL,
        resource_type VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL,
        allocated_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    print("Database schema created successfully!")
    return True

if __name__ == "__main__":
    create_tables()

