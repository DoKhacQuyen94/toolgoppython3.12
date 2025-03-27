# import os
# import time

# # Serial number hoặc IP của thiết bị
# ip = input("Nhập ip mạng của bạn: ")
# os.system("adb tcpip 5555")
# DEVICE = f"{ip}:5555"
# # Kết nối ADB
# os.system(f"adb connect {DEVICE}")

# def auto_click(x, y, times, delay):
#     for _ in range(times):
#         os.system(f"adb -s {DEVICE} shell input tap {x} {y}")
#         print(f"Clicked at ({x}, {y}) - Time {time.ctime()}")
#         time.sleep(delay)
# auto_click(220, 618, 1, 1)

import os
import time
import re

DEVICE = "192.168.1.8:5555"

def ensure_adb_connection():
    os.system(f"adb connect {DEVICE}")
    time.sleep(1)
    devices = os.popen("adb devices").read()
    if DEVICE not in devices:
        print(f"Failed to connect to {DEVICE}")
        exit(1)
    else:
        print(f"Connected to {DEVICE}")

ensure_adb_connection()

def find_text_coordinates(target_text):
    # Lấy dump giao diện
    os.system(f"adb -s {DEVICE} shell dumpsys window > dump.txt")
    with open("dump.txt", "r") as f:
        dump = f.read()
    
    # Tìm văn bản và tọa độ (dạng bounds="[x1,y1][x2,y2]")
    pattern = re.compile(r'(\[(\d+),(\d+)\]\[(\d+),(\d+)\]).*?' + re.escape(target_text), re.DOTALL)
    match = pattern.search(dump)
    if match:
        x1, y1, x2, y2 = int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))
        # Tính tọa độ giữa
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        return x, y
    else:
        print(f"Text '{target_text}' not found")
        return None

def click_text(target_text):
    coords = find_text_coordinates(target_text)
    if coords:
        x, y = coords
        os.system(f"adb -s {DEVICE} shell input tap {x} {y}")
        print(f"Clicked '{target_text}' at ({x}, {y}) - Time {time.ctime()}")
    else:
        print("Click failed")

# Thay "Click me" bằng văn bản bạn muốn click
click_text("Follow")