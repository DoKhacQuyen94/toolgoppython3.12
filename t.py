import os
import time
import xml.etree.ElementTree as ET

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
    # Lấy XML giao diện
    os.system(f"adb -s {DEVICE} shell uiautomator dump /sdcard/ui.xml")
    os.system(f"adb -s {DEVICE} pull /sdcard/ui.xml ui.xml")
    
    # Phân tích XML
    try:
        tree = ET.parse("ui.xml")
        root = tree.getroot()
        for node in root.iter("node"):
            if node.attrib.get("text") == target_text:
                bounds = node.attrib.get("bounds")  # Dạng [x1,y1][x2,y2]
                x1 = int(bounds.split("[")[1].split(",")[0])
                y1 = int(bounds.split("][")[0].split(",")[1])
                x2 = int(bounds.split("][")[1].split(",")[0])
                y2 = int(bounds.split("][")[1].split("]")[0].split(",")[1])
                x = (x1 + x2) // 2
                y = (y1 + y2) // 2
                return x, y
        print(f"Text '{target_text}' not found")
        return None
    except Exception as e:
        print(f"Error parsing UI: {e}")
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
