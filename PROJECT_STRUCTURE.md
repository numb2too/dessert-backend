# PROJECT_STRUCTURE.md

## 📁 專案結構說明

```
bakery-management-system/
│
├── app/                          # 應用程式核心目錄
│   ├── __init__.py              # 應用程式工廠函數
│   │
│   ├── models/                   # 資料模型（SQLAlchemy）
│   │   ├── __init__.py          # 員工、薪資、請假、績效模型
│   │   ├── finance.py           # 財務、材料、庫存模型
│   │   ├── sales_production_rd.py  # 銷售、生產、研發模型
│   │   └── user.py              # 使用者認證模型
│   │
│   ├── routes/                   # API 路由（藍圖）
│   │   ├── __init__.py          # 路由匯總
│   │   ├── auth.py              # 認證路由（登入、刷新）
│   │   ├── hr.py                # 人資路由（員工、薪資、請假、績效）
│   │   ├── finance.py           # 財務路由（材料、庫存、交易、報表）
│   │   ├── sales.py             # 銷售路由（客戶、訂單、統計）
│   │   ├── production.py        # 生產路由（批次、產能、進度）
│   │   └── rd.py                # 研發路由（食譜、材料配方）
│   │
│   ├── schemas/                  # 資料驗證與序列化（Marshmallow）
│   │   ├── auth.py              # 認證相關 Schema
│   │   ├── hr.py                # 人資相關 Schema
│   │   ├── finance.py           # 財務相關 Schema
│   │   ├── sales.py             # 銷售相關 Schema
│   │   ├── production.py        # 生產相關 Schema
│   │   └── rd.py                # 研發相關 Schema
│   │
│   ├── services/                 # 業務邏輯層（可選）
│   │   ├── hr_service.py        # 人資業務邏輯
│   │   ├── finance_service.py   # 財務業務邏輯
│   │   ├── sales_service.py     # 銷售業務邏輯
│   │   └── production_service.py # 生產業務邏輯
│   │
│   └── utils/                    # 工具函數
│       ├── decorators.py        # 自訂裝飾器
│       ├── validators.py        # 資料驗證器
│       └── helpers.py           # 輔助函數
│
├── tests/                        # 測試目錄
│   ├── conftest.py              # Pytest 配置與 Fixtures
│   ├── test_auth.py             # 認證測試
│   ├── test_hr.py               # 人資模組測試
│   ├── test_finance.py          # 財務模組測試
│   ├── test_sales.py            # 銷售模組測試
│   ├── test_production.py       # 生產模組測試
│   └── test_rd.py               # 研發模組測試
│
├── migrations/                   # 資料庫遷移腳本（Flask-Migrate）
│   ├── versions/                # 遷移版本
│   ├── alembic.ini             # Alembic 配置
│   └── env.py                  # 遷移環境設定
│
├── docker/                       # Docker 相關配置
│   ├── mysql/
│   │   └── init.sql            # MySQL 初始化腳本
│   └── nginx/
│       ├── nginx.conf          # Nginx 配置
│       └── ssl/                # SSL 憑證
│
├── .github/                      # GitHub 相關
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions CI/CD 流程
│
├── backups/                      # 資料庫備份目錄（不納入版控）
│
├── logs/                         # 日誌檔案（不納入版控）
│
├── config.py                     # 應用程式配置
├── wsgi.py                       # WSGI 應用程式入口
├── manage.py                     # 管理命令腳本
├── requirements.txt              # Python 依賴清單
├── Dockerfile                    # Docker 映像配置
├── docker-compose.yml            # Docker Compose 配置
├── docker-compose.prod.yml       # 生產環境 Docker 配置
├── .env.example                  # 環境變數範例
├── .gitignore                    # Git 忽略檔案
├── Makefile                      # 便捷命令
├── pytest.ini                    # Pytest 配置
├── README.md                     # 專案說明文檔
├── DEPLOYMENT.md                 # 部署指南
├── API_EXAMPLES.md               # API 使用範例
└── PROJECT_STRUCTURE.md          # 本檔案
```

## 🎯 核心目錄說明

### 📦 app/models/
資料模型定義，對應資料庫表結構。

**主要模型:**
- **Employee**: 員工基本資料
- **SalaryRecord**: 薪資變化紀錄
- **LeaveRecord**: 請假申請與審核
- **PerformanceRecord**: 績效評論
- **Material**: 材料庫存
- **MaterialStockMovement**: 庫存異動紀錄
- **FinancialTransaction**: 財務交易
- **Customer**: 客戶資料
- **Order**: 訂單主表
- **OrderItem**: 訂單明細
- **ProductionBatch**: 生產批次
- **ProductionItem**: 生產項目
- **Recipe**: 食譜
- **RecipeMaterial**: 食譜材料配方

### 🛣 app/routes/
API 端點定義，使用 APIFlask 藍圖。

**路由模組:**
- **auth.py**: `/api/auth/*` - 登入、Token 刷新
- **hr.py**: `/api/hr/*` - 員工、薪資、請假、績效管理
- **finance.py**: `/api/finance/*` - 材料、庫存、財務報表
- **sales.py**: `/api/sales/*` - 客戶、訂單管理
- **production.py**: `/api/production/*` - 生產批次、產能規劃
- **rd.py**: `/api/rd/*` - 食譜管理

### 📋 app/schemas/
資料驗證與序列化，使用 Marshmallow。

每個 Schema 定義了:
- **Input Schema**: 驗證輸入資料格式
- **Output Schema**: 定義回應資料結構
- **Query Schema**: 驗證查詢參數

### 🧪 tests/
單元測試與整合測試。

**測試結構:**
- `conftest.py`: 共用 fixtures（測試資料庫、測試客戶端等）
- `test_*.py`: 各模組的測試案例

### 🐳 Docker 相關
- **Dockerfile**: 應用程式容器映像
- **docker-compose.yml**: 開發環境服務編排
- **docker-compose.prod.yml**: 生產環境配置

## 🔑 關鍵檔案

### config.py
包含不同環境的配置：
- `DevelopmentConfig`: 開發環境
- `TestingConfig`: 測試環境
- `ProductionConfig`: 生產環境

### wsgi.py
Gunicorn 或其他 WSGI 伺服器的應用程式入口點。

### manage.py
提供管理命令：
- `seed-db`: 填充測試資料
- `create-admin`: 建立管理員帳號
- `init-db`: 初始化資料庫

## 🔄 資料流程

```
Client Request
      ↓
   Nginx (反向代理)
      ↓
   Gunicorn (WSGI Server)
      ↓
   Flask Application
      ↓
   API Blueprint (routes/)
      ↓
   Schema Validation (schemas/)
      ↓
   Business Logic (services/ or routes/)
      ↓
   Database Models (models/)
      ↓
   SQLAlchemy ORM
      ↓
   MySQL Database
```

## 📊 資料庫關聯圖

```
employees (員工)
    ├─→ salary_records (薪資)
    ├─→ leave_records (請假)
    └─→ performance_records (績效)

customers (客戶)
    └─→ orders (訂單)
           └─→ order_items (訂單項目)
                  └─→ production_items (生產項目)

recipes (食譜)
    ├─→ recipe_materials (食譜材料)
    │      └─→ materials (材料)
    └─→ order_items (訂單項目)

materials (材料)
    └─→ material_stock_movements (庫存異動)

production_batches (生產批次)
    └─→ production_items (生產項目)
```

## 🚀 開發工作流程

1. **建立功能分支**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **開發功能**
   - 在 `models/` 建立或修改資料模型
   - 在 `schemas/` 定義驗證規則
   - 在 `routes/` 實作 API 端點
   - 在 `tests/` 撰寫測試

3. **執行測試**
   ```bash
   make test
   ```

4. **資料庫遷移**
   ```bash
   make migration  # 建立遷移
   make migrate    # 套用遷移
   ```

5. **提交變更**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

6. **建立 Pull Request**
   - CI/CD 自動執行測試
   - Code Review
   - 合併到 develop/main 分支

## 📝 程式碼風格

- **Python**: PEP 8（使用 Black 格式化）
- **命名規範**:
  - 類別: `PascalCase`
  - 函數/變數: `snake_case`
  - 常數: `UPPER_SNAKE_CASE`
- **Docstring**: Google Style
- **Import 順序**: 標準庫 → 第三方庫 → 本地模組

## 🔐 安全注意事項

1. **環境變數**: 敏感資訊存放在 `.env`（不納入版控）
2. **密碼**: 使用 bcrypt 加密
3. **JWT Token**: 設定適當的過期時間
4. **SQL Injection**: 使用 SQLAlchemy ORM
5. **CORS**: 生產環境限制允許的 Origins

## 📚 延伸閱讀

- [Flask 官方文檔](https://flask.palletsprojects.com/)
- [APIFlask 文檔](https://apiflask.com/)
- [SQLAlchemy 文檔](https://docs.sqlalchemy.org/)
- [Pytest 文檔](https://docs.pytest.org/)
- [Docker 最佳實踐](https://docs.docker.com/develop/dev-best-practices/)