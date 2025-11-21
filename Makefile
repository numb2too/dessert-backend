.PHONY: help install dev test clean docker-build docker-up docker-down migrate seed lint format

# 預設目標
help:
	@echo "甜點店管理系統 - 可用命令："
	@echo ""
	@echo "  make install        - 安裝專案依賴"
	@echo "  make dev           - 啟動開發伺服器"
	@echo "  make test          - 執行測試"
	@echo "  make test-cov      - 執行測試並生成覆蓋率報告"
	@echo "  make lint          - 程式碼檢查"
	@echo "  make format        - 格式化程式碼"
	@echo "  make migrate       - 執行資料庫遷移"
	@echo "  make seed          - 填充測試資料"
	@echo "  make docker-build  - 建構 Docker 映像"
	@echo "  make docker-up     - 啟動 Docker 服務"
	@echo "  make docker-down   - 停止 Docker 服務"
	@echo "  make clean         - 清理快取檔案"
	@echo ""

# 安裝依賴
install:
	pip install -r requirements.txt

# 開發環境
dev:
	flask run --debug --host=0.0.0.0 --port=5000

# 執行測試
test:
	pytest -v

# 測試覆蓋率
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term
	@echo "覆蓋率報告已生成: htmlcov/index.html"

# 程式碼檢查
lint:
	flake8 app tests --max-line-length=120 --ignore=E203,W503
	@echo "✓ Flake8 檢查通過"

# 格式化程式碼
format:
	black app tests
	@echo "✓ 程式碼已格式化"

# 資料庫遷移
migrate:
	flask db upgrade

# 建立新的遷移
migration:
	@read -p "請輸入遷移描述: " desc; \
	flask db migrate -m "$$desc"

# 回滾遷移
rollback:
	flask db downgrade

# 填充測試資料
seed:
	python manage.py seed-db

# 建立管理員
admin:
	python manage.py create-admin

# Docker 相關
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "服務已啟動，請訪問 http://localhost:5000/docs"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f web

docker-shell:
	docker-compose exec web bash

docker-migrate:
	docker-compose exec web flask db upgrade

docker-seed:
	docker-compose exec web python manage.py seed-db

docker-test:
	docker-compose exec web pytest

# 生產環境
prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

# 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "✓ 已清理快取檔案"

# 備份資料庫
backup:
	@mkdir -p backups
	@filename="backups/backup_$$(date +%Y%m%d_%H%M%S).sql"; \
	docker-compose exec -T db mysqldump -u bakery_user -pbakery_pass bakery_dev > $$filename; \
	echo "✓ 資料庫已備份至: $$filename"

# 還原資料庫
restore:
	@read -p "請輸入備份檔案路徑: " file; \
	cat $$file | docker-compose exec -T db mysql -u bakery_user -pbakery_pass bakery_dev; \
	echo "✓ 資料庫已還原"

# 查看資料庫
db-shell:
	docker-compose exec db mysql -u bakery_user -pbakery_pass bakery_dev

# 初始化專案（首次使用）
init: install
	@echo "初始化專案..."
	@cp .env.example .env
	@echo "✓ 已建立 .env 檔案，請編輯設定"
	docker-compose up -d db
	@echo "等待資料庫啟動..."
	@sleep 10
	flask db upgrade
	python manage.py seed-db
	@echo ""
	@echo "✓ 專案初始化完成！"
	@echo "執行 'make dev' 啟動開發伺服器"
	@echo "或執行 'make docker-up' 使用 Docker 啟動"