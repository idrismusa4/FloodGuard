#!/usr/bin/env python3
"""
FloodGuardian AI Database Setup Script

This script initializes your Supabase database with all necessary tables and sample data.
Run this after setting up your Supabase project and updating your .env file.
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append('backend')

load_dotenv()

def main():
    print("🛡️ FloodGuardian AI Database Setup")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Missing Supabase configuration!")
        print("Please update your .env file with:")
        print("  SUPABASE_URL=https://your-project-id.supabase.co")
        print("  SUPABASE_KEY=your-service-role-key")
        return
    
    if "your-project-id" in supabase_url or "your-service-role-key" in supabase_key:
        print("❌ Error: Please replace placeholder values in .env file!")
        print("Current values:")
        print(f"  SUPABASE_URL={supabase_url}")
        print(f"  SUPABASE_KEY={supabase_key[:20]}...")
        return
    
    try:
        from supabase import create_client

        print(f"🔗 Connecting to Supabase...")
        # Just instantiate the client to validate URL/key formatting; avoid hitting non-existent tables
        _ = create_client(supabase_url, supabase_key)
        print("✅ Supabase client initialized")

        # Supabase schemas must be created via the SQL editor or migrations.
        # We generated a file 'supabase_schema.sql'. Please paste/run it in Supabase → SQL.
        print("\n📋 ACTION REQUIRED: Create tables in Supabase")
        print("   1) Open Supabase → SQL → New query")
        print("   2) Paste contents of supabase_schema.sql")
        print("   3) Click Run. Then re-run this script to seed sample users.")

        # Try to seed sample users; will fail gracefully if tables don't exist yet
        try:
            from supabase import create_client
            supabase = create_client(supabase_url, supabase_key)
            print("\n👥 Adding sample users (if table exists)...")
            sample_users = [
                {"name": "John Doe", "phone": "+2348012345678", "location": "Abuja"},
                {"name": "Jane Smith", "phone": "+2348012345679", "location": "Lagos"},
                {"name": "Ahmed Ibrahim", "phone": "+2348012345680", "location": "Kano"},
                {"name": "Grace Okoro", "phone": "+2348012345681", "location": "Port Harcourt"},
                {"name": "Fatima Hassan", "phone": "+2348012345682", "location": "Kaduna"},
            ]
            supabase.table("users").insert(sample_users).execute()
            print(f"  ✅ Sample users inserted")
        except Exception as e:
            print(f"  ℹ️  Skipped seeding (run after tables exist): {e}")

        print("\n🎉 Setup helper finished. Create tables via SQL, then re-run as needed.")

    except ImportError:
        print("❌ Error: supabase-py not installed!")
        print("Run: pip install supabase")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your Supabase URL and API key")

if __name__ == "__main__":
    main()
