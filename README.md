# Library-Seat-AI 圖書館座位感知監控系統 
這個系統的目的主要是用來實時判斷這個座位有沒有人坐，為了能達到這樣的目的，我在本地端電腦使用遷移學習，訓練了一個CNN model，叫做**MobileNetV3**，訓練好以後，我把它的參數儲存下來成.pt檔，接著轉移到raspberry pi 5，這樣我們就能在樹莓派中使用AI進行一些判斷及分類，最後我在樹莓派上面接上一台相機每隔5秒拍一次照，再傳回AI的程式碼中，就可以進行分類並輸出結果。


---

## 系統核心特點
1. **隱私保護與低功耗 (Snapshot Polling)**：系統不傳輸任何動態錄影串流上雲，而是由主控排程器定時（每 5 秒）擷取單張靜態影像，徹底保護現場讀者隱私並降低樹莓派 CPU 負載。
2. **AI 影像辨識**：在地端（raspberry pi 5）直接運作輕量化深度學習模型 **MobileNetV3**，於 2 秒內精準分類座位為「有人」或「無人」。
3. **AWS**：透過憑證，我們可以連接AWS的雲端服務，然後應用MQTT訂閱我們程式碼中設定的主題，就可以直接傳送到DynamoDB做管理。

---

## 系統架構 (System Architecture)
1. 樹莓派imx219 (120度) 攝像頭
2. raspberry pi 5
3. MobileNetV3 CNN
4. AWS

## 使用步驟
1. 使用SSH連接樹莓派
   ```bash
    ssh bjhd@rpi5-05.local
    # 或者輸入樹莓派的實際 IP 位址
    # ssh bjhd@<你的樹莓派IP>
2. 安裝樹莓派相機模組
   ```bash
   # 安裝相機模組
   sudo apt update
   sudo apt install rpicam-apps -y
3. 建立虛擬環境
   ```bash
   # 建立資料夾 (Make Directory)
   mkdir my_project

   # 切換進去該資料夾 (Change Directory)
   cd my_project
   
   # 建立虛擬環境 (若先前已建立則可跳過此行)
   python3 -m venv env

   # 啟動虛擬環境
   source env/bin/activate
4. 下載所有模組
   ```bash
   # 更新 pip 工具
   pip install --upgrade pip

   # 安裝 CPU 版本的 PyTorch 與 torchvision 輕量化套件
   pip install torch torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)

   # 安裝影像處理與 AWS IoT SDK
   pip install opencv-python Pillow awsiotsdk
5. 使用指令驅動python程式
   ```bash
   python3 main_loop.py
6. 使用 ctrl + c 結束程式！
