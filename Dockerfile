# 多階段構建 - 建立階段
FROM python:3.11-slim as builder

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir --user -r requirements.txt

# 執行階段
FROM python:3.11-slim

WORKDIR /app

# 安裝運行時依賴
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 從 builder 階段複製已安裝的套件
COPY --from=builder /root/.local /root/.local

# 確保腳本在 PATH 中
ENV PATH=/root/.local/bin:$PATH

# 複製應用程式代碼
COPY . .

# 建立非 root 使用者
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 暴露端口
EXPOSE 5000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# 啟動命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]