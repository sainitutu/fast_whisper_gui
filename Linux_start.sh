#!/bin/bash

# 設定虛擬環境名稱
VENV="whisperenv"

# 檢查虛擬環境資料夾是否存在
if [ ! -d "$VENV/bin" ]; then
    # 虛擬環境不存在，則創建它
    echo "Creating virtual environment..."
    python3 -m venv $VENV
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit $?
    fi
else
    echo "Virtual environment already exists."
fi

# 啟動虛擬環境
source $VENV/bin/activate

# 安裝 requirements.txt 中的套件
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install requirements."
    exit $?
fi

# 預備執行其他指令...
echo "Virtual environment is ready and packages are installed."

# 運行 main.py
python main.py
if [ $? -ne 0 ]; then
    echo "Failed to run main.py."
    exit $?
fi

read -p "Press enter to continue"
