import os
import time

# Serial number hoặc IP của thiết bị
ip = input("Nhập ip mạng của bạn: ")
os.system("adb tcpip 5555")
DEVICE = f"{ip}:5555"
# Kết nối ADB
os.system(f"adb connect {DEVICE}")

def auto_click(x, y, times, delay):
    for _ in range(times):
        os.system(f"adb -s {DEVICE} shell input tap {x} {y}")
        print(f"Clicked at ({x}, {y}) - Time {time.ctime()}")
        time.sleep(delay)
auto_click(220, 618, 1, 1)
