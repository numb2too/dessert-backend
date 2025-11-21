```bash
# 方法 1: 直接在容器內執行 (推薦)
docker-compose exec web pytest -v

# 方法 2: 明確設定環境變數
docker-compose exec -e TESTING=1 web pytest -v

# 方法 3: 進入容器後執行
docker-compose exec web bash
export TESTING=1
pytest -v
```

新增user
```bash
 curl -X POST http://127.0.0.1:5001/api/users/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Tony","email":"tony@test.com"}'
```