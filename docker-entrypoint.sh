#!/bin/sh
set -e

# --- 等待資料庫連線 (Wait for DB) ---
echo "Checking database connection..."

python << END
import socket
import time
import os
import sys
from urllib.parse import urlparse

# 1. 嘗試直接讀取 DB_HOST
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# 2. 如果沒有 DB_HOST，嘗試從 DATABASE_URL 解析
# 格式範例: mysql+pymysql://user:pass@gateway01...com:4000/dbname
if not host and os.getenv("DATABASE_URL"):
    try:
        url = urlparse(os.getenv("DATABASE_URL"))
        host = url.hostname
        port = url.port
        print(f"Parsed host from DATABASE_URL: {host}:{port}")
    except Exception as e:
        print(f"Failed to parse DATABASE_URL: {e}")

# 3. 如果還是沒有，使用預設值
host = host or "db"
port = int(port or 3306)

max_retries = 30
wait_seconds = 2

print(f"Waiting for database at {host}:{port}...")

for i in range(max_retries):
    try:
        with socket.create_connection((host, port), timeout=1):
            print(f"Database {host}:{port} is reachable!")
            sys.exit(0)
    except OSError:
        print(f"Connection failed... retrying in {wait_seconds}s ({i+1}/{max_retries})")
        time.sleep(wait_seconds)

sys.exit(1)
END

# --- 資料庫連線成功後，執行遷移 ---
echo "Running database migrations..."
flask db upgrade

# --- 啟動應用 ---
echo "Starting application..."
exec "$@"