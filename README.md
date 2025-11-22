# 甜點後台管理系統-後端
## Python + Flask/APIFlask 架構
### 功能
- rest api 後台
- 新增改查 USER

### 技能
- 透過 docker 運行 web & mysql
- web service 執行 rest api
- mysql database 連接
- pytest 做 unit test
- 透過 migrate 更新 mysql 欄位資訊
- MVC 架構
- github ci 自動測試
- 透過 debugpy 在 docker 運行下 使用 vscode 做斷點提升 debug 效率

## 執行
### docker (推薦)
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
> 使用 docker 啟動資料才會存到 mysql
> 因為 mysql 是跟 web 一起啟動
> 但有分不同 container 

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
啟動
```bash
python run.py
```
> 資料只存在 memory 沒有存到 mysql
> mysql 需透過 docker 開啟並連接

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