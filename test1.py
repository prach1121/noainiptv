from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.style import Style
import time
import psutil  # สำหรับตรวจสอบการใช้หน่วยความจำ
import requests  # สำหรับตรวจสอบสถานะอินเทอร์เน็ต

# สร้าง Console object
console = Console()

# ฟังก์ชันแสดงเวลาและวันที่
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%H:%M:%S"), now.strftime("%d/%m/%Y")

# ฟังก์ชันตรวจสอบสถานะอินเทอร์เน็ต
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return "เชื่อมต่ออินเทอร์เน็ต ✅"
    except requests.ConnectionError:
        return "ไม่เชื่อมต่ออินเทอร์เน็ต ❌"

# ฟังก์ชันตรวจสอบการใช้หน่วยความจำ
def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"ใช้หน่วยความจำ: {memory.used / 1024 / 1024:.2f} MB"

# ฟังก์ชันสร้าง Layout
def create_layout():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    return layout

# ฟังก์ชันอัปเดต UI
def update_ui(layout):
    time_now, date_now = get_current_time()
    internet_status = check_internet()
    memory_usage = get_memory_usage()

    # Header
    header = Panel(Text(f"Noain IPTV - ช่องรายการ", justify="center", style="bold blue"))
    layout["header"].update(header)

    # Main Content
    table = Table(title="ช่องรายการ", show_header=True, header_style="bold magenta")
    table.add_column("ช่อง", style="cyan", justify="center")
    table.add_column("รายการ", style="green")
    table.add_column("สถานะ", style="yellow")

    # ข้อมูลช่องรายการ (ตัวอย่าง)
    channels = [
        {"channel": "023", "program": "รายการข่าว", "status": "กำลังออกอากาศ"},
        {"channel": "024", "program": "ภาพยนตร์", "status": "หยุดออกอากาศ"},
        {"channel": "030", "program": "กีฬา", "status": "กำลังออกอากาศ"},
    ]

    for channel in channels:
        table.add_row(channel["channel"], channel["program"], channel["status"])

    layout["main"].update(table)

    # Footer
    footer = Panel(Text(
        f"เวลา: {time_now} | วันที่: {date_now} | {internet_status} | {memory_usage}",
        justify="center", style="bold green"
    ))
    layout["footer"].update(footer)

# ฟังก์ชันหลัก
def main():
    layout = create_layout()

    with Live(layout, refresh_per_second=1) as live:
        while True:
            update_ui(layout)
            time.sleep(1)

if __name__ == "__main__":
    main()
