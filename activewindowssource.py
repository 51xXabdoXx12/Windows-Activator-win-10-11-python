import tkinter as tk
from tkinter import ttk
import subprocess
import ctypes
import sys
import platform


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_windows_version():
    # استخدام platform للتحقق إذا كان النظام Windows 10 أو Windows 11
    version = platform.version()
    if "10" in version:
        return "Windows 10"
    elif "11" in version:
        return "Windows 11"
    else:
        return "Unknown"


def activate_windows():
    key_map = {
        # مفاتيح المنتج لـ Windows 10
        "Win 10 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "Win 10 Pro N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
        "Win 10 Edu": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
        "Win 10 Edu N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
        "Win 10 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
        "Win 10 Enterprise N": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
        "Win 10 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
        "Win 10 Home N": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
        "Win 10 Home Single Language": "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
        "Win 10 Home Country Specific": "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",

        # مفاتيح المنتج لـ Windows 11
        "Win 11 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",  # مفتاح منتج لـ Windows 11 Pro (مفتاح افتراضي)
        "Win 11 Pro N": "MH37W-N47XK-V7XM9-C7227-GCQG9",  # مفتاح منتج لـ Windows 11 Pro N (مفتاح افتراضي)
        "Win 11 Edu": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",  # مفتاح منتج لـ Windows 11 Edu (مفتاح افتراضي)
        "Win 11 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",  # مفتاح منتج لـ Windows 11 Enterprise (مفتاح افتراضي)
        "Win 11 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",  # مفتاح منتج لـ Windows 11 Home (مفتاح افتراضي)
        "Win 11 Home Single Language": "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",  # مفتاح منتج لـ Windows 11 Home Single Language (مفتاح افتراضي)
    }

    selected_option = combo.get()
    if selected_option not in key_map:
        result_label.config(text="Invalid selection.", fg="red")
        return

    product_key = key_map[selected_option]
    command = f"slmgr /ipk {product_key}"

    if subprocess.call(command, shell=True) != 0:
        result_label.config(text="Activation failed.", fg="red")
        return

    if subprocess.call("slmgr /skms kms8.msguides.com", shell=True) != 0:
        result_label.config(text="Activation failed.", fg="red")
        return

    if subprocess.call("slmgr /ato", shell=True) != 0:
        result_label.config(text="Activation failed.", fg="red")
        return

    result_label.config(text="Windows activated successfully.", fg="green")


def activate_button_clicked():
    if is_admin():
        activate_windows()
    else:
        result_label.config(text="Please run the script as administrator.", fg="red")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


window = tk.Tk()
window.title("Windows Activation")
window.geometry("300x250")

# التحقق من إصدار Windows
current_version = get_windows_version()
edition_label = ttk.Label(window, text=f"Current Windows Version: {current_version}")
edition_label.pack(pady=10)

instruction_label = ttk.Label(window, text="Choose the Windows version to activate:")
instruction_label.pack(pady=10)

# تغيير الخيارات بناءً على الإصدار المكتشف
if current_version == "Windows 10":
    options = [
        "Win 10 Pro",
        "Win 10 Pro N",
        "Win 10 Edu",
        "Win 10 Edu N",
        "Win 10 Enterprise",
        "Win 10 Enterprise N",
        "Win 10 Home",
        "Win 10 Home N",
        "Win 10 Home Single Language",
        "Win 10 Home Country Specific"
    ]
elif current_version == "Windows 11":
    options = [
        "Win 11 Pro",
        "Win 11 Pro N",
        "Win 11 Edu",
        "Win 11 Enterprise",
        "Win 11 Home",
        "Win 11 Home Single Language"
    ]
else:
    options = []

combo = ttk.Combobox(window, values=options, width=30)
combo.pack(pady=10)
combo.current(0)

activate_button = ttk.Button(window, text="Activate Windows", command=activate_button_clicked)
activate_button.pack(pady=20)

result_label = ttk.Label(window, text="", foreground="black")
result_label.pack()

window.mainloop()
