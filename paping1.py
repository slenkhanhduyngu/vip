import socket
import time
import sys
import argparse
import requests
def tcp_ping(host, port, timeout=1):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    start_time = time.time()
    try:
        s.connect((host, port))
        elapsed_time = time.time() - start_time
        s.close()
        return round(elapsed_time * 1000) 
    except socket.error:
        return None
def main():

    parser = argparse.ArgumentParser(description="TCP Ping Tool")
    parser.add_argument("host", type=str, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port")
    
    args = parser.parse_args()

    try:
        response = requests.get(f"http://ip-api.com/json/{args.host}")
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success':
            print(f"\033[1;32mCountry: \033[0m{data['country']}")
            print(f"\033[1;32mCountry Code: \033[0m{data['countryCode']}")
            print(f"\033[1;32mRegion Name: \033[0m{data['regionName']}")
            print(f"\033[1;32mCity: \033[0m{data['city']}")
            print(f"\033[1;32mTimezone: \033[0m{data['timezone']}")
            print(f"\033[1;32mAS: \033[0m{data['as']}")
        else:
            print("Không thể lấy thông tin IP. Lỗi:", data['message'])
    except requests.RequestException as e:
        print(f"Xảy ra lỗi khi kết nối tới dịch vụ IP API: {e}")
    print("---------------------------------------------------------")
    time.sleep(2.5)
    attempted = 0
    connected = 0
    total_time = 0
    min_time = float('inf')
    max_time = 0

    try:
        while True:
            attempted += 1
            result = tcp_ping(args.host, args.port)
            if result:
                connected += 1
                total_time += result
                min_time = min(min_time, result)
                max_time = max(max_time, result)
                print(f"\033[0mConnected to \033[1;32m{args.host}\033[0m: \033[0mtime=\033[1;32m{result}ms \033[0mprotocol=\033[1;32mTCP \033[0mport=\033[1;32m{args.port}\033[0m")
            else:
                print(f"\033[1;31mConnection timeout\033[0m")
            time.sleep(1)  
    except KeyboardInterrupt:
        failed = attempted - connected
        average_time = total_time / connected if connected != 0 else 0

        print("\nConnection statistics:")
        print(f"\tAttempted = {attempted}, Connected = {connected}, Failed = {failed} ({(failed/attempted)*100:.2f}%)")
        print("Approximate connection times:")
        print(f"\tMinimum = {min_time:.2f}ms, Maximum = {max_time:.2f}ms, Average = {average_time:.2f}ms")
        sys.exit(0)

if __name__ == "__main__":
    main()