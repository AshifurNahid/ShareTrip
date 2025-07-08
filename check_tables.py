import sqlite3
import os
import sys
import subprocess

def check_django_installation():
    """Check if Django is installed and provide setup guidance"""
    print("=== Environment Check ===")
    
    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"Virtual environment active: {'Yes' if in_venv else 'No'}")
    print(f"Python executable: {sys.executable}")
    
    # Check for virtual environment folder
    venv_exists = os.path.exists('venv') or os.path.exists('.venv')
    print(f"Virtual environment folder found: {'Yes' if venv_exists else 'No'}")
    
    # Check Django installation
    try:
        import django  # type: ignore
        print(f"✅ Django is installed (version: {django.get_version()})")
        return True
    except ImportError:
        print("❌ Django is not installed")
        print("\n🔧 To fix this issue, run these commands in order:")
        
        if not venv_exists:
            print("\n1. Create a virtual environment:")
            print("   python -m venv venv")
        
        print("\n2. Activate the virtual environment:")
        if os.name == 'nt':  # Windows
            print("   .\\venv\\Scripts\\activate")
        else:  # Unix/Linux/Mac
            print("   source venv/bin/activate")
        
        print("\n3. Install Django:")
        print("   pip install django")
        
        # Check for requirements.txt
        if os.path.exists('requirements.txt'):
            print("\n4. Install project dependencies:")
            print("   pip install -r requirements.txt")
        else:
            print("\n4. You may also need to install other packages like:")
            print("   pip install pillow  # for image handling")
            print("   pip install django-crispy-forms  # if using forms")
        
        print("\n5. Then run migrations and start the server:")
        print("   python manage.py migrate")
        print("   python manage.py runserver")
        
        return False

def check_database():
    """Check database tables"""
    print("\n=== Database Check ===")
    
    # Check if database file exists
    if os.path.exists('db.sqlite3'):
        print("Database file found!")
        
        # Connect to database
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Check specific tables
        expected_tables = ['users', 'trips', 'bookings', 'trips_tripimage']
        print("\nChecking for your custom tables:")
        for table_name in expected_tables:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            result = cursor.fetchone()
            if result:
                print(f"✅ {table_name} - EXISTS")
            else:
                print(f"❌ {table_name} - NOT FOUND")
        
        conn.close()
    else:
        print("❌ Database file not found!")
        print("Run 'python manage.py migrate' after setting up Django to create the database.")

def check_database_data():
    """Check database tables and actual data"""
    print("\n=== Database Data Check ===")
    
    if not os.path.exists('db.sqlite3'):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check Django auth tables for users
    try:
        cursor.execute("SELECT COUNT(*) FROM auth_user;")
        user_count = cursor.fetchone()[0]
        print(f"Django Users: {user_count}")
        
        if user_count > 0:
            cursor.execute("SELECT id, username, email, is_superuser FROM auth_user;")
            users = cursor.fetchall()
            print("Users found:")
            for user in users:
                user_type = "Admin" if user[3] else "Regular"
                print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Type: {user_type}")
    except sqlite3.OperationalError:
        print("❌ auth_user table not found - run migrations first")
    
    # Check custom tables
    custom_tables = ['users_user', 'trips_trip', 'bookings_booking']
    for table in custom_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")
        except sqlite3.OperationalError:
            print(f"❌ {table} table not found")
    
    conn.close()

def offer_auto_setup():
    """Offer to automatically set up the environment"""
    print("\n" + "="*50)
    setup = input("Would you like me to help set up the environment? (y/n): ").lower().strip()
    
    if setup == 'y':
        try:
            # Create virtual environment if it doesn't exist
            if not (os.path.exists('venv') or os.path.exists('.venv')):
                print("\n📦 Creating virtual environment...")
                subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
                print("✅ Virtual environment created!")
            
            # Provide activation instructions
            print("\n🔧 Next steps:")
            print("1. Activate the virtual environment by running:")
            if os.name == 'nt':
                print("   .\\venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
            
            print("2. Then install Django:")
            print("   pip install django")
            
            if os.path.exists('requirements.txt'):
                print("3. Install dependencies:")
                print("   pip install -r requirements.txt")
            
            print("4. Run migrations and start server:")
            print("   python manage.py migrate")
            print("   python manage.py runserver")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    django_available = check_django_installation()
    check_database()
    check_database_data()
    
    if not django_available:
        print("\n⚠️  Please install Django before running 'python manage.py runserver'")
        offer_auto_setup()
