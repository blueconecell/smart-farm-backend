import serial
import requests
import logging
import sys
import json

# 서버 URL 설정 (샘플별로 다른 엔드포인트 사용)
server_urls = [
    "http://192.168.129.191:8000/api/v1/smallFarm/GasAreaSample/1",
    "http://192.168.129.191:8000/api/v1/smallFarm/GasAreaSample/2",
    "http://192.168.129.191:8000/api/v1/smallFarm/GasAreaSample/3",
    "http://192.168.129.191:8000/api/v1/smallFarm/GasAreaSample/4"
]

# 시리얼 포트 설정 (포트와 보드레이트는 실제 환경에 맞게 조정 필요)
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

# 수신된 데이터 파싱 함수
def parse_received_data(received_data):
    # 수신된 데이터를 공백으로 분리하여 각 센서 값 추출
    data_parts = received_data.split(',')
    parsed_data = []
    
    for part in data_parts:
        part = part.strip()  # Remove leading and trailing whitespace
        if ':' in part:
            sensor, value = part.split(':', 1)  # Split only once
            sensor = sensor.strip()
            value = value.strip()
            
            # 단위가 포함된 값에서 단위 제거하지 않음
            if ' mg/L' in value:
                value = value.replace(' mg/L', '').strip()
            
            try:
                # Convert value to float
                data = {
                    'sensor': sensor,
                    'value': float(value),  # 숫자 값만 변환
                    'unit': 'mg/L'  # 단위를 따로 추가
                }
                parsed_data.append(data)
            except ValueError:
                logging.error(f"Invalid data format for value: {value}")
    
    return parsed_data

# 서버로 데이터 전송 함수
def send_data_to_server(data):
    # 각 센서 데이터를 서버에 POST 요청으로 보내기
    for i, item in enumerate(data):
        if i < len(server_urls):  # Ensure we have a corresponding URL
            json_data = {
                "gasValue": item['value'],
                "gasArea_sample": i + 1,  # gasArea_sample은 1부터 시작
                "unit": item['unit']  # 단위 포함
            }
            
            headers = {'Content-Type': 'application/json'}
            
            try:
                response = requests.post(server_urls[i], json=json_data, headers=headers)
                logging.info(f"Sent data: {json_data}")
                logging.info('Status code: %d', response.status_code)
                logging.info('Response: %s', response.text)
            except requests.RequestException as e:
                logging.error(f"Error sending data to server: {e}")
        else:
            logging.error(f"No server URL for index {i}")

def main():
    logging.basicConfig(level=logging.INFO)
    
    while True:
        try:
            if ser.in_waiting > 0:
                # LoRa로부터 수신된 데이터 읽기
                received_data = ser.readline().decode('utf-8').strip()
                logging.info(f"Received: {received_data}")
                
                # 수신된 데이터 파싱
                parsed_data = parse_received_data(received_data)
                
                # 각 센서 데이터를 서버로 POST 요청 보내기
                send_data_to_server(parsed_data)
        
        except KeyboardInterrupt:
            logging.info("Script terminated by user")
            ser.close()
            sys.exit(0)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()