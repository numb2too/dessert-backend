# Koyeb

## 完整的 **從 GitHub 到 Koyeb** 的部署流程懶人包。

---

### 第一階段：事前檢查 (GitHub)

在去 Koyeb 之前，請確保你的程式碼已經推送到 GitHub，且包含以下關鍵檔案設定：

1.  **`requirements.txt`**：
    必須包含 `gunicorn`, `pymysql`, `cryptography`。
2.  **`Dockerfile`**：
    確保最後一行的指令有加上 Log 設定（方便除錯），且 Port 是 8000：
    ```dockerfile
    CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
    ```
3.  **推送到 GitHub**：
    ```bash
    git add .
    git commit -m "Ready for deployment"
    git push origin main
    ```

    > 我這邊是用 release merge 到 main 觸發部署

---

### 第二階段：Koyeb 設定 (Console 操作)

1.  **登入 Koyeb**：前往 [Koyeb Control Panel](https://app.koyeb.com/)。
2.  **建立新服務**：點擊 **"Create Service"**。
3.  **選擇來源 (Source)**：
    *   選擇 **GitHub**。
    *   選擇你的專案儲存庫 (Repository)。
    *   分支 (Branch) 選 `main`。
4.  **設定建置方式 (Builder)**：
    *   選擇 **Dockerfile** (因為我們有寫 Dockerfile)。
    *   Build command 跟 Run command 留空即可 (會自動讀取 Dockerfile)。
5.  **環境變數 (Environment Variables)** 🔴 **(最重要的一步)**：
    點擊 "Add Variable"，新增以下三個：

    | Key            | Value                 | 說明                               |
    | :------------- | :-------------------- | :--------------------------------- |
    | `FLASK_ENV`    | `production`          | 告訴 Flask 這是正式環境            |
    | `PORT`         | `8000`                | 雖然 Gunicorn 設定了，但加著保險   |
    | `DATABASE_URL` | `mysql+pymysql://...` | **請填入 TiDB 給你的完整連線字串** |

    > **⚠️ 關於 DATABASE_URL 的特別提醒：**
    > 這裡的連線字串 **必須包含** SSL 憑證路徑。
    > 格式應類似：
    > `mysql+pymysql://user:pass@host:4000/test?ssl_ca=/etc/ssl/certs/ca-certificates.crt&ssl_verify_cert=true&ssl_verify_identity=true`
    >
    > **為什麼？** 因為 Koyeb 的環境是 Linux，它裡面真的有 `/etc/ssl/certs/ca-certificates.crt` 這個檔案，這跟你的 Mac 不一樣。

6.  **設定端口 (Instance / Ports)**：
    *   **Port**: `8000` (必須對應 Dockerfile 裡的設定)。
    *   **Protocol**: HTTP。
    *   **Public path**: `/`。
7.  **部署**：
    *   給 App 取個名字 (例如 `your-service-api`)。
    *   點擊 **"Deploy"**。

---

### 第三階段：驗證與測試

1.  **觀察部署日誌 (Logs)**：
    *   點擊 "Logs" 分頁。
    *   你會看到 Docker Image 正在 Build (安裝 pip 套件...)。
    *   等到看見 **`[INFO] Listening at: http://0.0.0.0:8000`**，代表服務啟動成功！

2.  **取得公開網址**：
    *   在 Dashboard 上方會看到一個類似 `https://yourname.koyeb.app` 的網址。

3.  **測試 API**：
    *   打開瀏覽器或 Postman。
    *   測試 GET：`https://你的網址.koyeb.app/api/users/`
    *   如果回傳 JSON (空陣列 `[]` 或你剛剛遷移進去的資料)，恭喜你！部署成功！
  
---

### 常見錯誤排除

*   **錯誤：`Health check failed` 或 部署變紅燈**
    *   **原因**：通常是 Port 沒對上。檢查 Dockerfile 是不是寫 8000，Koyeb 設定是不是也是 8000。
    *   **原因**：資料庫連不上。檢查 Logs，如果有