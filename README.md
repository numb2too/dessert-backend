# 甜點後台管理系統-後端
## Python + Flask/APIFlask 架構
### 功能
- rest api 後台
- 增刪改查 USER
- 自動生成 API docs 
  - http://127.0.0.1:5001/docs

### 技能
- 透過 docker 運行 web & mysql
- web service 執行 rest api
- mysql database 連接
- pytest 做 unit test
- 透過 migrate 更新 mysql 欄位資訊
- MVC 架構
- github ci 自動測試
- 透過 debugpy 在 docker 運行下 使用 vscode 做斷點提升 debug 效率
- 透過 APIFlask 自動生成 api 文件
- api error_handlers 統一回傳格式

## 執行
### docker compose (推薦)
確認 docker 資訊
```bash
docker info
```
沒有資訊的話先安裝
```bash
brew install --cask docker
# install 中途斷掉的話 reinstall
brew reinstall --cask docker
```
安裝成功確認有 docker info 後 執行 compose up
```bash
docker compose up --build
```

### python
```bash
# 1. 建立名為 venv 的虛擬環境
python -m venv venv

# 2. 啟動虛擬環境
# Mac/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```
需先安裝
```bash
pip install -r requirements.txt
```
啟動資料庫
```bash
docker-compose up -d db
```
```bash
# 確保已啟動虛擬環境並安裝套件
python run.py
# 也可使用
flask run --port 5001
```
> 結果：App 跑在 http://localhost:5001。
> 原理：讀取 .env，透過 127.0.0.1:3306 連到 Docker 資料庫。

### docker
```bash
docker build -t dessert-api .
```
可本地測試
```bash
docker run --rm \
  -p 5001:8000 \
  --env PORT=8000 \
  --env DATABASE_URL="mysql+pymysql://your_user:your_password@host.docker.internal:3306/your_db" \
  your-container-name 
```

## unit test
### 簡單確認 API
```bash
curl -X POST http://127.0.0.1:5001/api/users/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Amy","email":"amy@test.com"}'
```
成功會回傳
```bash
{
  "email": "amy@test.com",
  "id": 5,
  "name": "Amy",
  "phone": null
}
```
### pytest
python 直接測試 pytest
```bash
dessert-backend % pytest
================================================== test session starts ==================================================
platform darwin -- Python 3.13.7, pytest-9.0.1, pluggy-1.6.0
rootdir: /Users/qq/dessert-backend
collected 6 items                                                                                                       

tests/test_user_routes.py ...                                                                                     [ 50%]
tests/test_user_service.py ...                                                                                    [100%]

=================================================== 6 passed in 0.17s =====
```
使用 docker pytest
```bash
dessert-backend % docker-compose exec web pytest                                                        
================================================================ test session starts ================================================================
platform linux -- Python 3.13.9, pytest-9.0.1, pluggy-1.6.0
rootdir: /app
collected 21 items                                                                                                                                  

tests/test_user_routes.py ...........                                                                                                         [ 52%]
tests/test_user_service.py ..........                                                                                                         [100%]

================================================================ 21 passed in 0.11s    
```