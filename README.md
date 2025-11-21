# 🍰 甜點店員工成本管理系統

基於 Flask + APIFlask + MySQL 的完整後端管理系統，包含人資、財務、銷售、生產、研發五大模組。

## 📋 目錄

- [功能特色](#功能特色)
- [技術架構](#技術架構)
- [快速開始](#快速開始)
- [API 文檔](#api-文檔)
- [測試](#測試)
- [部署](#部署)

## ✨ 功能特色

### 🧑‍💼 人資模組 (HR)
- ✅ 員工基本資料管理
- ✅ 薪資紀錄與變化追蹤
- ✅ 請假管理與審核流程
- ✅ 績效評論紀錄
- ✅ 職務執掌管理

### 💰 財務模組 (Finance)
- ✅ 蛋糕製作成本計算
- ✅ 材料庫存管理（含異動紀錄）
- ✅ 財務交易紀錄
- ✅ 即時盈利與成本分析
- ✅ 財務報表生成

### 🛒 銷售模組 (Sales)
- ✅ 客戶資料管理（含 VIP 標記）
- ✅ 訂單管理與查詢
- ✅ 訂單優先級排序
- ✅ 訂單與客戶資料快速鉤稽
- ✅ 訂單生產進度追蹤
- ✅ 銷售統計報表

### 🏭 生產模組 (Production)
- ✅ 生產批次管理
- ✅ 每日產能規劃
- ✅ 生產進度追蹤
- ✅ 訂單生產項目管理

### 🔬 研發模組 (R&D)
- ✅ 食譜管理（含版本控制）
- ✅ 食譜材料配方
- ✅ 食譜快速查詢與篩選
- ✅ 製作難度與時間估算

## 🛠 技術架構

### 後端技術棧
- **Web 框架**: Flask 3.0 + APIFlask 2.1
- **資料庫**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **認證**: JWT (Flask-JWT-Extended)
- **資料驗證**: Marshmallow
- **測試**: Pytest + Coverage
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **WSGI 伺服器**: Gunicorn

### 專案架構
```
bakery-management-system/
├── app/                    # 應用程式核心
│   ├── models/            # 資料模型
│   ├── routes/            # API 路由
│   ├── schemas/           # 資料驗證 Schema
│   ├── services/          # 業務邏輯服務
│   └── utils/             # 工具函數
├── tests/                 # 單元測試
├── migrations/            # 資料庫遷移
├── docker/                # Docker 配置
│   ├── mysql/
│   └── nginx/
├── .github/workflows/     # CI/CD 配置
├── requirements.txt       # Python 依賴
├── Dockerfile            # 應用程式容器
├── docker-compose.yml    # 服務編排
├── config.py             # 配置管理
├── wsgi.py              # WSGI 入口
└── manage.py            # 管理命令
```

## 🚀 快速開始

### 前置需求
- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0+ (若不使用 Docker)

### 1. 克隆專案
```bash
git clone https://github.com/yourusername/bakery-management-system.git
cd bakery-management-system
```

### 2. 環境設定
```bash
# 複製環境變數範例
cp .env.example .env

# 編輯 .env 檔案，設定資料庫連線等資訊
vim .env
```

### 3. 使用 Docker Compose 啟動（推薦）
```bash
# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f web

# 執行資料庫遷移
docker-compose exec web flask db upgrade

# 填充測試資料
docker-compose exec web python manage.py seed-db

# 建立管理員帳號
docker-compose exec web python manage.py create-admin
```

應用程式將在 `http://localhost:5000` 啟動

### 4. 本地開發模式
```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 填充測試資料
python manage.py seed-db

# 啟動開發伺服器
flask run
```

## 📚 API 文檔

啟動應用後訪問:
- **Swagger UI**: http://localhost:5000/docs
- **OpenAPI Spec**: http://localhost:5000/openapi.json

### 主要端點

#### 認證
```
POST   /api/auth/login      # 登入
POST   /api/auth/refresh    # 刷新 Token
GET    /api/auth/me         # 取得當前使用者
```

#### 人資管理
```
GET    /api/hr/employees                    # 員工列表
POST   /api/hr/employees                    # 新增員工
GET    /api/hr/employees/{id}               # 員工詳情
PATCH  /api/hr/employees/{id}               # 更新員工
GET    /api/hr/employees/{id}/salaries      # 薪資紀錄
POST   /api/hr/employees/{id}/performance   # 新增績效評論
GET    /api/hr/leave-records                # 請假紀錄
POST   /api/hr/leave-records                # 申請請假
```

#### 銷售管理
```
GET    /api/sales/customers           # 客戶列表
POST   /api/sales/customers           # 新增客戶
GET    /api/sales/orders              # 訂單列表（支援排序與篩選）
POST   /api/sales/orders              # 新增訂單
GET    /api/sales/orders/{id}         # 訂單詳情（含客戶資料與生產進度）
PATCH  /api/sales/orders/{id}/priority  # 更新訂單優先級
GET    /api/sales/statistics/sales-summary  # 銷售統計
```

#### 財務管理
```
GET    /api/finance/materials         # 材料庫存
POST   /api/finance/materials         # 新增材料
GET    /api/finance/materials/{id}/movements  # 庫存異動紀錄
GET    /api/finance/transactions      # 財務交易
GET    /api/finance/reports/profit-loss  # 損益報表
```

#### 生產管理
```
GET    /api/production/batches        # 生產批次
POST   /api/production/batches        # 建立生產批次
GET    /api/production/daily-capacity  # 每日產能
PATCH  /api/production/items/{id}/complete  # 完成生產項目
```

#### 研發管理
```
GET    /api/rd/recipes                # 食譜列表
POST   /api/rd/recipes                # 新增食譜
GET    /api/rd/recipes/{id}           # 食譜詳情（含材料配方）
PATCH  /api/rd/recipes/{id}           # 更新食譜
GET    /api/rd/recipes/search         # 搜尋食譜
```

### 認證方式
所有 API（除了登入）都需要 JWT Token:
```bash
# 1. 登入取得 Token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "emp001", "password": "password123"}'

# 2. 使用 Token 訪問 API
curl -X GET http://localhost:5000/api/hr/employees \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 測試

### 執行所有測試
```bash
# 使用 Docker
docker-compose exec web pytest

# 本地執行
pytest
```

### 測試覆蓋率
```bash
# 生成覆蓋率報告
pytest --cov=app --cov-report=html --cov-report=term

# 查看 HTML 報告
open htmlcov/index.html
```

### 測試特定模組
```bash
pytest tests/test_hr.py         # 測試人資模組
pytest tests/test_sales.py      # 測試銷售模組
pytest tests/test_auth.py       # 測試認證
```

## 🚢 部署

### Docker 部署（推薦）

#### 1. 建構映像
```bash
docker build -t bakery-management:latest .
```

#### 2. 使用 Docker Compose 部署
```bash
# 生產環境
docker-compose -f docker-compose.yml --profile production up -d

# 包含 Nginx 和 Redis
docker-compose -f docker-compose.prod.yml up -d
```

### 手動部署

#### 1. 設定環境變數
```bash
export FLASK_ENV=production
export DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret-key
```

#### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

#### 3. 資料庫遷移
```bash
flask db upgrade
```

#### 4. 啟動應用
```bash
# 使用 Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app

# 或使用 uWSGI
uwsgi --http 0.0.0.0:5000 --module wsgi:app --processes 4
```

### Nginx 反向代理配置
```nginx
server {
    listen 80;
    server_name api.bakery.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 CI/CD

專案使用 GitHub Actions 實現自動化 CI/CD:

### CI 流程
1. **程式碼檢查**: Flake8, Black
2. **單元測試**: Pytest + Coverage
3. **Docker 建構**: 自動建構映像
4. **測試環境部署**: 自動部署到 staging

### CD 流程
- **Develop 分支**: 自動部署到測試環境
- **Main 分支**: 自動部署到生產環境（需人工審核）

查看 `.github/workflows/ci-cd.yml` 了解詳細配置。

## 📊 資料庫 Schema

### 核心資料表
- `employees`: 員工資料
- `salary_records`: 薪資紀錄
- `leave_records`: 請假紀錄
- `performance_records`: 績效評論
- `materials`: 材料庫存
- `material_stock_movements`: 庫存異動
- `financial_transactions`: 財務交易
- `customers`: 客戶資料
- `orders`: 訂單
- `order_items`: 訂單項目
- `production_batches`: 生產批次
- `production_items`: 生產項目
- `recipes`: 食譜
- `recipe_materials`: 食譜材料關聯

查看 `app/models/` 目錄了解完整資料模型。

## 🤝 貢獻指南

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權

MIT License

## 👥 聯絡資訊

專案維護者: Your Name
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**注意**: 這是一個練習專案，但採用業界標準的架構設計。在生產環境使用前，請確保:
- 更改所有預設密碼和金鑰
- 配置適當的資料庫備份
- 設定監控和日誌系統
- 實施適當的安全措施（HTTPS、防火牆等）
- 進行完整的安全審計