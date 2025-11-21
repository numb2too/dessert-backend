# 甜點ERP管理系統後台
## Python + Flask/APIFlask 架構

```bash
project/
├── app.py                # 主程式入口
├── routes/
│   └── user_routes.py    # 使用者的 API
├── services/
│   └── user_service.py   # 商業邏輯
└── models/
    └── user_model.py     # 模擬資料
```

## 執行
需先安裝
```bash
pip install apiflask
```
啟動
```bash
python app.py
```

## 測試
```bash
curl http://127.0.0.1:5000/api/users/1
```
```bash
curl -X POST http://127.0.0.1:5000/api/users/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Tony","email":"tony@test.com"}'
```