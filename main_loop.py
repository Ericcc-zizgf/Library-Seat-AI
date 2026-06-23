import os
import time
t = 5

def main():
    print("==================================================")
    print("   🚀 智慧圖書館座位監控系統 - 全自動排程已啟動   ")
    print("==================================================")
    print(f"提示：系統將每 {t} 秒自動輪詢一次。按下 Ctrl+C 可安全中斷\n")
    
    loop_count = 1
    
    try:
        while True:
            print(f"\n─────────────────── [第 {loop_count} 次感測] ───────────────────")
            
            # 讓系統去呼叫你的「拍照 + AI」流程
            exit_code = os.system("python3 take_photo.py")
            
            if exit_code != 0:
                print("[警告] 此次輪詢流程發生異常，將於下次重試。")
            
            print(f"\n⏳ 流程結束，等待 {t} 秒後進行下一次感測...")
            time.sleep(t)  # 這裡就是你設定的 t 秒休息時間
            
            loop_count += 1
            
    except KeyboardInterrupt:
        print("\n\n==================================================")
        print("   🛑 接收到手動中斷指令，系統已安全關閉。   ")
        print("==================================================")

if __name__ == "__main__":
    main()