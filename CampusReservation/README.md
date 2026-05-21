# 🎓 校園空間預約與資源管理系統 (Campus Reservation System)

本系統是一個基於 **Python Flask** 與 **SQLite** 開發的輕量級校園空間與設備資源管理系統。前端整合了 **Bootstrap 5** 與 **Chart.js**，提供直觀的數據統計儀表板。

---

## 💻 系統環境需求
- **Python 3.6 或以上版本** (請確認安裝時有勾選 `Add Python to PATH` 以便在命令列使用)。

---

## 🚀 快速啟動說明

### 🔹 方法一：Windows 使用者 (最簡單)
我們已在專案目錄下提供 `雙擊啟動.bat` 檔案。
1. 直接**按兩下 (雙擊) 執行** `雙擊啟動.bat`。
2. 系統會自動完成：
   - 檢查 Python 環境。
   - 自動安裝必要依賴套件 (`Flask`)。
   - 自動偵測並初始化 SQLite 資料庫。
   - 自動開啟瀏覽器並開啟網頁，開始執行程式。
3. **欲結束程式**：直接關閉黑色的命令列視窗即可。

---

### 🔹 方法二：命令列手動啟動 (Windows / macOS 均適用)
請打開終端機 (Terminal) 或命令提示字元 (cmd)，切換至專案根目錄，並依序執行以下指令：

```bash
# 1. 切換至專案資料夾 (請更換為您的實際路徑)
cd CampusReservation

# 2. 安裝必要依賴套件
pip install -r requirements.txt

# 3. 初始化資料庫 (若已存在 database.db 則會略過)
python init_db.py

# 4. 啟動 Flask 伺服器
python app.py
```
啟動成功後，打開瀏覽器並訪問：  
👉 **`http://127.0.0.1:5000`**

---

## 🔑 預設測試帳號

系統提供以下兩組不同權限的測試帳號（密碼皆為 `1234`）：

| 身分 | 登入 Email | 密碼 | 說明 |
| :--- | :--- | :--- | :--- |
| **管理員 (Admin)** | `admin@school.edu` | `1234` | 可以查看所有預約、取消所有人的預約、觀看全校設備統計。 |
| **學生 (Student)** | `student@school.edu` | `1234` | 只能看到並取消自己的預約紀錄、進行空間與設備的預約。 |

---

## 📁 專案目錄結構
```
CampusReservation/
├── app.py                  # Flask 主程式，處理路由與預約衝突邏輯
├── init_db.py              # 資料庫初始化與測試資料寫入腳本
├── requirements.txt        # 專案套件依賴清單 (Flask 及其套件)
├── 雙擊啟動.bat             # Windows 專用的快速啟動批次檔
├── README.md               # 專案使用說明文檔
├── static/
│   ├── css/
│   │   └── style.css       # 客製化樣式設計 (包含卡片懸浮效果等)
│   └── js/
│       └── main.js         # 前端 Chart.js 動態渲染邏輯
└── templates/
    ├── login.html          # 系統登入介面
    ├── index.html          # 空間狀態儀表板 (圓餅圖 + 長條圖 + 預約表)
    └── book.html           # 預約表單頁面 (整合防衝突檢測)
```
