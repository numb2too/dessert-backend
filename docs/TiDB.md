
# TiDB Cloud
TiDB Cloud 提供免費額度，且高度相容 MySQL  
以下是完整的串接步驟，分為 **「取得連線資訊」**、**「本機遷移資料」**、**「Koyeb 部署設定」** 三個階段。

## 第一階段：在 TiDB Cloud 取得連線字串

1.  **註冊/登入**：前往 [TiDB Cloud](https://tidbcloud.com/) 並登入。
2.  **建立 Cluster**：
    *   點擊 "Create Cluster"。
    *   選擇 免費 的方案即可。
    *   Region 建議選 **AWS - Tokyo (東京)**，離台灣最近，連線速度快。
3.  **設定密碼**：
    *   建立時會要求你設定 Root Password，**請記下來**。
4.  **取得連線字串**：
    *   Cluster 建立好後（幾秒鐘），點擊右上角的 **"Connect"**。
    *   Connect With 選擇 **"SQLAlchemy"**。
    *   Operating System 選擇 **"Linux"** (因為 Koyeb 是 Linux 環境)。
    *   你會得到一串類似這樣的網址：
        ```text
        mysql+pymysql://<使用者名稱>:<密碼>@<host>:4000/test?ssl_ca=/etc/ssl/certs/ca-certificates.crt&ssl_verify_cert=true&ssl_verify_identity=true
        ```

**⚠️ 注意事項：**
*   **Port 是 4000**：TiDB 預設是用 4000，不是 3306。
*   **SSL 設定**：TiDB Cloud 強制要求加密連線。
*   **資料庫名稱**：預設通常是 `test`，你可以把網址中的 `/test` 改成 `/dessert_db` (但通常要先連進去 Create Database，或者直接用預設的 `test` 也可以)。

---

## 第二階段：準備依賴與本機測試

TiDB 的認證機制比較新，且強制 SSL，所以你需要確保 `requirements.txt` 有包含必要的套件。

1.  **修改 `requirements.txt`**：
    加入 `cryptography` (如果還沒有的話)，這是安全連線必須的。
    ```text
    flask
    flask-sqlalchemy
    flask-migrate
    pymysql
    cryptography  <-- 必須加這個
    python-dotenv
    apiflask
    gunicorn
    ```

2.  **安裝更新**：
    ```bash
    pip install -r requirements.txt
    ```

---

## 第三階段：執行資料庫遷移 (從本機操作雲端)

你的雲端資料庫現在是空的。我們要在本機電腦下指令，把 Table 結構「推」到 TiDB 上。

1.  **複製你的 TiDB 連線字串**，並將密碼填入。
    例如：`mysql+pymysql://2Hxxxx.root:MyPassword@gateway01...:4000/test?ssl_ca=/etc/ssl/certs/ca-certificates.crt&ssl_verify_cert=true&ssl_verify_identity=true`

    > **Mac 使用者的小技巧**：
    > Mac 本機可能沒有 `/etc/ssl/certs/ca-certificates.crt` 這個檔案。
    > **在本機執行遷移時**，你可以暫時把 `?` 後面的參數簡化為 `?ssl_mode=VERIFY_IDENTITY` 或者乾脆拿掉 `ssl_ca` 參數試試看 (因為本機 Python 通常會自動抓系統憑證)。
    >
    > **本機測試用的字串建議：**
    > `mysql+pymysql://<user>:<pass>@<host>:4000/test?ssl={"ssl_mode":"VERIFY_IDENTITY"}`

2.  **執行遷移指令 (不修改 .env 的做法)**：
    在終端機直接設定暫時的環境變數來執行 `upgrade`。

    ```bash
    # Mac 
    export export DATABASE_URL="mysql+pymysql://<user>:<pass>@<host>:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    # 確認連線正常
    flash db init
    # 更新
    flash db upgrade
    ```

    *如果成功，你會看到 Alembic 正在建立 users table 的訊息。*

---

## 第四階段：Koyeb 部署設定 (生產環境)

現在要告訴 Koyeb 上的程式去連 TiDB。

1.  **進入 Koyeb 控制台** -> 你的 App -> **Settings** -> **Environment Variables**。
2.  **修改 `DATABASE_URL`**：
    *   填入 TiDB 提供的 **完整連線字串** (包含 `ssl_ca=/etc/ssl/certs/ca-certificates.crt` 那一長串)。
    *   **重要**：Koyeb 是 Linux 環境，所以它絕對有 `/etc/ssl/certs/ca-certificates.crt` 這個檔案，**請務必保留 SSL 參數**，否則會連線失敗。
3.  **確認其他變數**：
    *   `FLASK_ENV`: `production`
    *   `PORT`: `8000` (如果用 Gunicorn)
4.  **重新部署 (Redeploy)**。

---

## 常見問題排除 (Troubleshooting)

**Q1: 報錯 `ModuleNotFoundError: No module named 'cryptography'`**
*   **解法**：確認 `requirements.txt` 有加入 `cryptography`，且已重新 `docker build` 或重新部署。

**Q2: 報錯 `ssl.SSLCertVerificationError` (在本機)**
*   **解法**：這是因為 Mac 的憑證路徑跟 Linux 不同。
    在本機測試時，你可以把 `DATABASE_URL` 裡的 `ssl_ca=...` 參數拿掉，改成 `ssl_mode=PREFERRED` 試試，或者直接不加參數 (pymysql 有時會自動處理)。
    **但在 Koyeb 上一定要加完整的 SSL 參數。**

**Q3: 報錯 `Unknown database 'dessert_db'`**
*   **解法**：TiDB 預設只有 `test` 資料庫。
    你可以把連線字串裡的 `/dessert_db` 改成 `/test`。
    或者先用 MySQL Client 連進去執行 `CREATE DATABASE dessert_db;`。

**Q4: 怎麼確認有沒有連成功？**
*   看 Koyeb 的 Logs。如果 Gunicorn 成功啟動且沒有噴 SQL 連線錯誤，那就是成功了。
*   你也可以用 API Postman 打打看，如果能新增使用者，代表資料寫入 TiDB 了。


## 自己補充
### mysql
#### 創 api user
```bash
CREATE USER 'username'@'%' IDENTIFIED BY 'your_password';
```

#### 查看所有使用者
```bash
SELECT User, Host FROM mysql.user;
```

#### 給予權限
當我確認連線成功後  
我有先重新創建一個權限比較正常的 user   
之後都用這個 user 做 api 連接 mysql 的帳號  
減少 root 的資安風險  
```bash
GRANT SELECT, INSERT, UPDATE, DELETE
ON your_db_name.*
TO 'your_user_name'@'%';
FLUSH PRIVILEGES;
```

❌請避免
```bash
GRANT ALL PRIVILEGES ON *.* TO 'api_user'@'%';
```
這會讓 API 具備 root 級別權限，包含整個 MySQL server 所有資料庫。  
很危險，除非是本機測試用途。  

#### 查看使用者權限
```bash
SHOW GRANTS FOR 'username'@'%';
```

### migrate
#### 有 migrate 資料夾導致更新失敗
刪除資料夾
```bash
flask db init
flask db migrate -m "init tables"
flask db upgrade
```

#### 「版本錯亂」問題
開發環境的資料不先刪除
可以嘗試這個方法
但我最後資料還是刪了QQ
```bash
docker-compose up -d db
flask db stamp head
flask db upgrade
```

##### 發生原因
1.  **你的資料庫 (Docker 內)** 還記得上次的最後一個版本號是 `92d1973a1ea7` (因為它儲存在資料庫裡的 `alembic_version` 資料表中)。
2.  **你的程式碼 (migrations 資料夾)** 剛剛被你刪掉重來了，所以裡面**已經沒有** `92d1973a1ea7` 這個檔案了。
3.  **衝突**：當你執行指令時，Flask 去問資料庫：「你現在幾版？」資料庫回：「我是 `92d1973a1ea7`。」Flask 回頭找資料夾：「咦？我找不到這個檔案啊？」於是就報錯 `Can't locate revision...`。

---

##### 解決方法：刪除資料庫的版本記憶

我們需要手動把資料庫裡的「版本紀錄表 (`alembic_version`)」刪掉，讓它以為自己是全新的，然後再蓋上新的印章。

請依照以下步驟操作（最簡單的方式是用 `flask shell`）：

###### 步驟 1：進入 Flask Shell 刪除版本紀錄表

確保你的 `.env` 是連到 **本機 Docker** (`127.0.0.1`)，然後在終端機執行：

```bash
flask shell
```

進入互動介面後（會看到 `>>>`），依序輸入以下 Python 程式碼：

```python
from app import db
from sqlalchemy import text

# 1. 刪除紀錄版本的 table (不會影響你的 users 資料)
db.session.execute(text("DROP TABLE IF EXISTS alembic_version"))

# 2. 確認執行
db.session.commit()

# 3. 離開
exit()
```

###### 步驟 2：重新標記版本 (Stamp)

現在資料庫已經「失憶」了，我們要告訴它：「你現在就是最新的版本」。

在終端機執行：

```bash
flask db stamp head
```

這次應該就會出現 `INFO ... Stamp revision ...` 的成功訊息，而不會報錯了。

###### 步驟 3：確認同步

最後檢查一次：

```bash
flask db upgrade
```

預期結果：它應該會說沒有東西需要更新 (因為已經 stamp 過了)，這樣就代表你的 **本機程式碼** 與 **本機資料庫** 再次同步了！