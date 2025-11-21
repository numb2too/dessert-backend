# 甜點ERP管理系統後台
## Python + Flask/APIFlask 架構

```bash
project/
├── app.py
├── routes/
│   └── user_routes.py
├── services/
│   └── user_service.py
├── models/
│   └── user_model.py
├── tests/
│   ├── test_user_service.py
│   └── test_user_routes.py
└── requirements.txt

```

## 執行
需先安裝
```bash
pip install -r requirements.txt
```
啟動
```bash
python app.py
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