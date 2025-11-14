"""
Migration script to add Event model and update Device model
Run this after updating the models.py file
"""
from sqlalchemy import create_engine, text
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import settings
from app.database import Base
from app.models import Event, Device

def run_migration():
    """Run the migration"""
    engine = create_engine(settings.DATABASE_URL)
    
    print("Running migration: add_events_and_update_devices")
    
    with engine.connect() as conn:
        # Add new columns to devices table
        try:
            print("Adding new columns to devices table...")
            conn.execute(text("""
                ALTER TABLE devices 
                ADD COLUMN IF NOT EXISTS last_connected TIMESTAMP,
                ADD COLUMN IF NOT EXISTS health_status VARCHAR(20) DEFAULT 'unknown',
                ADD COLUMN IF NOT EXISTS event_count INTEGER DEFAULT 0;
            """))
            conn.commit()
            print("✓ Device columns added successfully")
        except Exception as e:
            print(f"Note: {e}")
        
        # Create events table
        try:
            print("Creating events table...")
            Base.metadata.tables['events'].create(engine, checkfirst=True)
            print("✓ Events table created successfully")
        except Exception as e:
            print(f"Note: {e}")
    
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    run_migration()
