@echo off

REM 設定虛擬環境名稱
set VENV=whisperenv

REM 檢查虛擬環境資料夾是否存在
if not exist "%VENV%\Scripts\activate.bat" (
    REM 虛擬環境不存在，則創建它
    echo Creating virtual environment...
    python -m venv %VENV%
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        exit /b %ERRORLEVEL%
    )
) else (
    echo Virtual environment already exists.
)

REM 啟動虛擬環境
call %VENV%\Scripts\activate.bat

REM 安裝 requirements.txt 中的套件
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install requirements.
    exit /b %ERRORLEVEL%
)

REM 預備執行其他指令...
echo Virtual environment is ready and packages are installed.

REM 運行 main.py
python main.py
if %ERRORLEVEL% neq 0 (
    echo Failed to run main.py.
    exit /b %ERRORLEVEL%
)

pause