import serial
import requests
from urllib.parse import urlencode
import logging
import sys

# 서버 URL 설정
server_url = "http://172.20.10.2:8000/api/v1/smallFarm/MoistureSensor"

# 시리얼 포트 설정 (포트와 보드레이트는 실제 환경에 맞게 조정 필요)
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

# 센서 번호와 농경지 이름 매핑
# sensor_map = {
#     'S1': '1차 농경지',
#     'S2': '2차 농경지',
#     'S3': '3차 농경지',
#     'S4': '4차 농경지'
# }
sensor_map = {
    'S1': 1,
    'S2': 2,
    'S3': 3,
    'S4': 4
}

def parse_received_data(received_data):
    # 수신된 데이터를 공백으로 분리하여 각 센서 값 추출
    data_parts = received_data.split()
    parsed_data = []

    for part in data_parts:
        if ':' in part:  # ':'가 포함된 부분만 처리
            sensor, value = part.split(':')
            if sensor in sensor_map:
                try:
                    data = {
                        'soil_sample': sensor_map[sensor],
                        'humidValue': float(value)
                    }
                    parsed_data.append(data)
                except ValueError:
                    logging.error(f"Invalid data format for value: {value}")
    
    return parsed_data

def send_data_to_server(data):
    # JSON 형식이 아닌 application/x-www-form-urlencoded 형식으로 데이터 변환
    form_data = urlencode(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(server_url, data=form_data, headers=headers)
        logging.info(f"Sent data: {data}")
        logging.info('상태 코드: %d', response.status_code)
        logging.info('응답: %s', response.text)
    except requests.RequestException as e:
        logging.error(f"Error sending data to server: {e}")

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
                for data in parsed_data:
                    send_data_to_server(data)
        
        except KeyboardInterrupt:
            logging.info("Script terminated by user")
            ser.close()
            sys.exit(0)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
