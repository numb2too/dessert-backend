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