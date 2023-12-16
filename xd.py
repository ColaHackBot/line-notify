import requests
import json
import time
from datetime import datetime
import pytz  # เพิ่มไลบรารี pytz เข้ามาในโค้ด

# ค่า URL API และ Token ของ Line Notify
line_notify_token = "UEYTMjAuWSQ15AMkNaSahCAuSBVojZD90atPQ37JumJ"
line_notify_api = "https://notify-api.line.me/api/notify"

# ฟังก์ชันสำหรับส่งข้อความแจ้งเตือนไปยัง Line Notify
def send_line_notification(message):
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }
    payload = {
        "message": message
    }
    requests.post(line_notify_api, headers=headers, data=payload)

# ฟังก์ชันสำหรับตรวจสอบและแจ้งเตือนการเปลี่ยนแปลงข้อมูลสินค้า
def check_product_changes():
    last_product_data = {}  # เก็บข้อมูลสินค้าล่าสุดเพื่อเปรียบเทียบ
    while True:
        try:
            response = requests.get("https://byshop.me/api/product")
            if response.status_code == 200:
                product_data = response.json()
                if last_product_data:
                    for product in product_data:
                        product_id = product["id"]
                        product_name = product["name"]
                        product_price = product["price"]
                        product_stock = product["stock"]

                        last_product = last_product_data.get(product_id)
                        if last_product:
                            if (last_product["name"] != product_name or
                                    last_product["price"] != product_price or
                                    last_product["stock"] != product_stock):
                                # ส่งการแจ้งเตือนเมื่อมีการเปลี่ยนแปลงข้อมูล
                                thailand_timezone = pytz.timezone('Asia/Bangkok')  # เลือก timezone ของประเทศไทย
                                thailand_time = datetime.now(thailand_timezone).strftime("%d/%m/%Y %H:%M:%S")  # ดึงเวลาประเทศไทย
                                message = f"ร้าน Byshop\nสินค้า ID: {product_id}\nชื่อ: {product_name}\nราคา: {product_price}\nคงเหลือ: {product_stock}\nอัพเดทล่าสุดเมื่อ: {thailand_time}\nซื้อของที่ https://byshop.me/buy/?page=agentshop"
                                send_line_notification(message)

                        last_product_data[product_id] = {
                            "name": product_name,
                            "price": product_price,
                            "stock": product_stock
                        }

                else:
                    # กำหนดค่าข้อมูลสินค้าล่าสุดหากยังไม่มีข้อมูล
                    for product in product_data:
                        product_id = product["id"]
                        product_name = product["name"]
                        product_price = product["price"]
                        product_stock = product["stock"]

                        last_product_data[product_id] = {
                            "name": product_name,
                            "price": product_price,
                            "stock": product_stock
                        }

            time.sleep(1)  # ตั้งค่าให้ตรวจสอบข้อมูลทุก 1 วินาที
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {str(e)}")
            time.sleep(1)  # หยุดสักครู่เพื่อป้องกันการเกิดข้อผิดพลาดที่เกินไป

if __name__ == "__main__":
    check_product_changes()
