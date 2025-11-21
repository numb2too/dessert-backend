FROM python:3.13-slim

WORKDIR /app

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 設定環境變數
ENV PYTHONPATH=/app
ENV FLASK_APP=run.py

# 開放端口
EXPOSE 5000

# 啟動應用
CMD ["python", "run.py"]