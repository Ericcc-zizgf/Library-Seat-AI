import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import cv2
import os
import time
from datetime import datetime
import json


from awscrt import mqtt
from awsiot import mqtt_connection_builder
ENDPOINT = "a3j57ftnswweby-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "MyIotThing"
TOPIC = "seat_status"

PATH_TO_CERT = "device.pem.crt"  
PATH_TO_KEY = "private.pem.key"       
PATH_TO_ROOT_CA = "Amazon-root-CA-1.pem" 

IMAGE_NAME = "seat_capture.jpg"

# =====================================================================
# 1. 模型架構定義
# =====================================================================
class MobileNetV3_LibrarySeat(nn.Module):
    def __init__(self, num_classes=2):
        super(MobileNetV3_LibrarySeat, self).__init__()
        self.backbone = models.mobilenet_v3_large(weights=None) 
        in_features = self.backbone.classifier[3].in_features
        self.backbone.classifier[3] = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.4),
            nn.Linear(128, num_classes)
        )
    def forward(self, x):
        return self.backbone(x)

def main():
    print("\n=== 步驟二：執行 AI 模型辨識 ===")
    
    # 檢查照片是否存在
    if not os.path.exists(IMAGE_NAME):
        print(f"❌【錯誤】找不到 {IMAGE_NAME}，請確認拍照是否成功！")
        return

    device = torch.device("cpu")
    print("正在載入 MobileNetV3 AI 模型...")
    
    # 載入模型（關閉安全性檢查）
    model = torch.load("mobilenetv3_library_seat.pt", map_location=device, weights_only=False)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    classes = ["座位無人", "座位有人"] 

    # 讀取剛才拍好的照片
    print("正在分析照片中...")
    pil_img = Image.open(IMAGE_NAME).convert('RGB')
    input_tensor = transform(pil_img).unsqueeze(0).to(device)

    # 進行 AI 推論
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs, 1)
        current_status = classes[predicted.item()]
    
    print(f"\n【辨識結果】: {current_status}\n")
    # --- MQTT 上傳至 AWS IoT Core ---
    print("\n☁️  正在連線至 AWS IoT Core...")
    try:
        # 建立 MQTT 連線
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERT,
            pri_key_filepath=PATH_TO_KEY,
            ca_filepath=PATH_TO_ROOT_CA,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=30
        )
        
        connect_future = mqtt_connection.connect()
        connect_future.result() # 等待連線成功
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 封裝成極輕量的 JSON 格式 (完美呼應你的 Figure 4 架構)
        payload = {
            "seat_id": "Seat-005",
            "status": current_status,
            "timestamp": current_time_str
        }

        # 發布訊息到指定 Topic
        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        print(f"✅ 【MQTT 傳送成功】: {payload}")

        # 安全斷線釋放資源
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()

    except Exception as e:
        print(f"❌ 【AWS 傳輸失敗】: 請檢查網路連線或憑證路徑。詳細錯誤：{e}")

if __name__ == "__main__":
    main()