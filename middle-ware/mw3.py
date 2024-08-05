import serial
import requests
import json
import re

# 시리얼 포트 설정
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)

# 서버 URL
server_url = "http://172.20.10.2:8000/api/v1/smallFarm/"

# 요청 헤더
headers = {"Content-Type": "application/json"}


def send_soil_value_to_server(name, value):
    data = {"name": name, "soil_humid": value}
    try:
        # POST 요청 보내기
        response = requests.post(server_url, data=json.dumps(data), headers=headers)
        # 응답 출력
        if response.status_code == 200:
            print("서버에 데이터가 성공적으로 전송되었습니다.")
            print("응답:", response.text)
        else:
            print("데이터 전송 실패.")
            print("상태 코드:", response.status_code)
            print("응답:", response.text)
    except requests.RequestException as e:
        print("오류가 발생했습니다:", e)


try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            print(f"Received: {line}")
            # 정규 표현식으로 'n차 농경지, soil_humid: value' 또는 'n차 농경지, humid: value' 형태의 데이터를 매칭
            match = re.search(r"(\d+)차 농경지,\s*(?:soil_humid|humid):\s*(\d+)", line)
            if match:
                field_number = match.group(1)
                moisture_value = int(match.group(2))
                field_name = f"{field_number}차 농경지"
                print(f"Extracted moisture value: {moisture_value} from {field_name}")
                send_soil_value_to_server(field_name, moisture_value)
except KeyboardInterrupt:
    pass
finally:
    ser.close()
