import os
import time

ENDPOINT = "a3j57ftnswweby-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "MyIotThing"

IMAGE_NAME = "seat_capture.jpg"

def main():
    print("=== 步驟一：開始現場拍照 ===")
    
    # 1. 暴力清除相機殘留行程 (隱藏錯誤訊息)
    os.system("sudo killall -9 rpicam-jpeg rpicam-hello rpicam-vid libcamera-vid 2>/dev/null")
    time.sleep(1) 

    print("正在啟動 IMX219 鏡頭...")
    
    # 2. 執行系統拍照指令
    cmd = f"rpicam-jpeg --output {IMAGE_NAME} --width 640 --height 480 -t 1000"
    exit_code = os.system(cmd)
    
    if exit_code == 0:
        print(f"\n✅【拍照成功】照片已儲存為: {IMAGE_NAME}\n")
        print("=== 準備呼叫 AI 模型程式 ===")
        
        # 3. 拍照成功後，立刻讓 Python 去呼叫另一個 AI 辨識檔案！
        os.system("python3 predict_photo.py")
        
    else:
        print(f"\n❌【錯誤】相機拍照失敗，系統錯誤代碼: {exit_code}\n")

if __name__ == "__main__":
    main()