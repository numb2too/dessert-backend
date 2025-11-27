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

### 啟動 mysql 
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

### 連線到測試資料庫
```bash
docker compose exec your-container mysql -u your_user -p
```

### dockerfile
- 連接本地 db 執行 dockerfile
```bash
docker run --rm \
  -p 5001:8000 \
  --env PORT=8000 \
  --env DATABASE_URL="mysql+pymysql://your_user:your_password@host.docker.internal:3306/your_db" \
  your-container-name
```

## 更新 requirements.txt
```bash
pip freeze > requirements.txt
```

## migrate 更新 db column
### 初始化（如果還沒做過）
做一次就好
```bash
flask db init
```

### 產生 migration
```bash
flask db migrate -m "add phone column"
```

### 套用到資料庫
```bash
flask db upgrade
```

### 修改版本好
如果不小心刪除 migrate 資料夾
查詢目前的版本號
```bash
flask db history
```
修改版本好
```bash
docker compose exec <docker-container-name> mysql -u your_user -p your_database -e "UPDATE alembic_version SET version_num='ed1234kjadfc3';"
```

## database

查詢已有的 user
```bash
SELECT User, Host FROM mysql.user;
```
建立使用者
```bash
CREATE USER 'your_user'@'%' IDENTIFIED BY 'your_password';
```
設定權限
```bash
GRANT SELECT, INSERT, UPDATE, DELETE
ON dessert.*
TO 'your_user'@'%';
FLUSH PRIVILEGES;
```


