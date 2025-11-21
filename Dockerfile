FROM python:3.13-slim

WORKDIR /app

# 安裝 wait-for-it
RUN apt-get update && apt-get install -y wait-for-it && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 設定環境變數
ENV PYTHONPATH=/app
ENV FLASK_APP=run.py

# 開放端口
EXPOSE 5001

# 啟動應用（等待 db:3306 就緒後再啟動）
CMD ["wait-for-it", "db:3306", "--", "python", "run.py"]