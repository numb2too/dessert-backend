FROM python:3.13-slim

WORKDIR /app

# 只安裝 MySQL 客戶端工具（如果需要的話）
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 複製專案程式碼
COPY . .

# 設定環境變數
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# 開放端口
EXPOSE 8000

# 啟動應用
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "120", "run:app"]