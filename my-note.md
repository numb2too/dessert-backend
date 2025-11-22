## docker
### 環境確認
```bash
docker info 

# 查看運行中的 container
docker ps

# 查看所有 container（包含已停止的）
docker ps -a

# 查看 container 的 log
docker-compose logs

# 進入 container 內部
docker exec -it <container_name> bash

# 停止所有 container
docker-compose down

# 停止並刪除 volume
docker-compose down -v

# 重新建置並啟動
docker-compose up --build
```

**查看所有 image：**
```bash
docker images
```

**刪除專案相關 image：**
```bash
docker-compose down --rmi all
```

**刪除所有未使用的 image：**
```bash
docker image prune -a
```

**完全關閉 Docker Desktop：**

方法 1：點選選單列的 Docker 鯨魚圖示 → Quit Docker Desktop

方法 2：指令關閉
```bash
osascript -e 'quit app "Docker"'
```

### container
停止 container
```bash
docker stop 9233d30b794c
```
刪除 container
```bash
docker rm my-mysql
```

### mysql 
```bash
# 拉取最新 MySQL 映像
docker pull mysql:8.0

# 建立並啟動容器
docker run -d \
  --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=YOUR_ROOT_PASSWORD \
  -e MYSQL_DATABASE=YOUR_DATABASE \
  -e MYSQL_USER=YOUR_USER \
  -e MYSQL_PASSWORD=YOUR_PASSWORD \
  -p 3306:3306 \
  mysql:8.0
```
> 帳號密碼記得修改

進入容器 MySQL：
```bash
docker exec -it my-mysql mysql -u root -p
```

## 更新 requirements.txt
```bash
pip freeze > requirements.txt
```

## migrate 更新 db column
```bash
# 設定環境變數
# 進入 web 容器執行 flask db init
docker compose exec web flask db init

# 產生 migration
docker compose exec web flask db migrate -m "add phone column"

# 套用到資料庫
docker compose exec web flask db upgrade
```