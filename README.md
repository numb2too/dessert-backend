# 甜點ERP管理系統後台
## Python + Flask/APIFlask 架構

## 執行
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

### docker 
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

## unit test
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