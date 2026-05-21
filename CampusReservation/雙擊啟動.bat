@echo off
chcp 65001 >nul
echo ===================================================
echo   校園空間預約與資源管理系統 - 快速啟動腳本
echo ===================================================
echo.

:: 1. 檢查 Python 是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 偵測不到 Python！請確認您的電腦已安裝 Python 並將其加入系統變數 (PATH)。
    echo 您可以從 https://www.python.org/ 下載最新版的 Python 安裝。
    echo 安裝時請務必勾選 "Add Python to PATH" 選項。
    echo.
    pause
    exit /b
)

:: 2. 安裝必要套件
echo [1/3] 正在檢查與安裝必要套件 (Flask)...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [警告] 依賴安裝失敗，嘗試直接安裝 Flask...
    pip install Flask
)

:: 3. 確保資料庫初始化
if not exist database.db (
    echo [2/3] 偵測到資料庫不存在，正在初始化資料庫...
    python init_db.py
) else (
    echo [2/3] 資料庫已就緒。
)

:: 4. 啟動伺服器並自動開啟網頁
echo [3/3] 正在啟動 Flask 伺服器...
echo 伺服器啟動後，請在瀏覽器輸入 http://127.0.0.1:5000 進行訪問。
echo 欲關閉系統，請直接關閉此黑白視窗。
echo.

:: 延遲 2 秒後開啟瀏覽器
start "" http://127.0.0.1:5000
python app.py

pause
