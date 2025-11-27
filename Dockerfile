FROM python:3.13-slim

WORKDIR /app

# 只安裝 MySQL 客戶端工具（如果需要的話）
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# 複製專案程式碼
COPY . .

# --- 新增的部分開始 ---
# 複製 entrypoint 腳本並給予執行權限
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# 設定環境變數
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV FLASK_APP=run.py


EXPOSE 8000

# 設定 Entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]

# CMD 保持不變，作為參數傳遞給 Entrypoint
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "run:app"]