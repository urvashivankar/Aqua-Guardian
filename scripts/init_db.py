import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Add backend to path
sys.path.append(str(Path.cwd() / "backend"))
from db.supabase import supabase

# Load env
env_path = Path.cwd() / "backend" / ".env"
print(f"Loading env from: {env_path}")
print(f"File exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path, override=True)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL and env_path.exists():
    print("⚠️ load_dotenv failed, trying manual parse...")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"File content length: {len(content)}")
            for line in content.splitlines():
                print(f"Line: {repr(line)}")
                line = line.strip()
                if "DATABASE_URL" in line:
                    print(f"Found DATABASE_URL in line: {line}")
                    if "=" in line:
                        DATABASE_URL = line.split("=", 1)[1]
                        print(f"Extracted: {DATABASE_URL[:10]}...")
                        break
    except Exception as e:
        print(f"Error reading file: {e}")

if not DATABASE_URL:
    print("⚠️ Using hardcoded fallback DATABASE_URL")
    DATABASE_URL = "postgresql://postgres:Urvashi%401603@db.hsoooexgsnxsvyfnwuef.supabase.co:6543/postgres?sslmode=require"

print(f"DATABASE_URL found: {bool(DATABASE_URL)}")

def run_schema_migration():
    print("🚀 Starting database migration...")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in .env")
        return False

    urls_to_try = []
    
    # Try original URL
    if DATABASE_URL:
        urls_to_try.append(DATABASE_URL)
        if ":6543" in DATABASE_URL:
            urls_to_try.append(DATABASE_URL.replace(":6543", ":5432"))
            
    # Try resolving hostname to IP
    try:
        import socket
        from urllib.parse import urlparse
        
        parsed = urlparse(DATABASE_URL)
        hostname = parsed.hostname
        if hostname:
            print(f"Resolving {hostname}...")
            ip = socket.gethostbyname(hostname)
            print(f"Resolved to {ip}")
            
            # Construct URL with IP
            url_with_ip = DATABASE_URL.replace(hostname, ip)
            urls_to_try.append(url_with_ip)
            if ":6543" in url_with_ip:
                urls_to_try.append(url_with_ip.replace(":6543", ":5432"))
    except Exception as e:
        print(f"⚠️ DNS resolution failed: {e}")

    for url in urls_to_try:
        try:
            # Mask password for logging
            safe_url = url
            if "@" in safe_url:
                parts = safe_url.split("@")
                safe_url = "..." + parts[1]
            
            print(f"Trying to connect to {safe_url}...")
            conn = psycopg2.connect(url, connect_timeout=10)
            cur = conn.cursor()
            
            schema_path = Path.cwd() / "backend" / "db" / "schema.sql"
            with open(schema_path, "r") as f:
                schema_sql = f.read()
                
            print("Running SQL commands...")
            cur.execute(schema_sql)
            conn.commit()
            
            cur.close()
            conn.close()
            print("✅ Database schema applied successfully.")
            return True
        except Exception as e:
            print(f"⚠️ Database migration failed with URL: {e}")
            
    print("❌ All database connection attempts failed.")
    return False

def create_storage_bucket():
    print("🚀 Creating storage bucket 'photos'...")
    try:
        # Check if bucket exists
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        
        if "photos" in bucket_names:
            print("✅ Bucket 'photos' already exists.")
        else:
            res = supabase.storage.create_bucket("photos", options={"public": True})
            print(f"✅ Bucket 'photos' created: {res}")
            
    except Exception as e:
        print(f"❌ Failed to create storage bucket: {e}")

if __name__ == "__main__":
    # Run both independently
    run_schema_migration()
    create_storage_bucket()
