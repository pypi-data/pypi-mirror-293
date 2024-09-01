import hashlib
import datetime
import barcode
from barcode.writer import ImageWriter
import os
import time
import uuid
import subprocess

# Fungsi untuk memverifikasi lisensi
def verify_license(user_id, license_key):
    secret_key = "kunci_rahasia_anda"
    try:
        license_key, expiration_timestamp = license_key.split('-')
        expiration_timestamp = int(expiration_timestamp)
        if datetime.datetime.now().timestamp() > expiration_timestamp:
            delete_license_file()
            return False
        raw_string = f"{user_id}{expiration_timestamp}{secret_key}"
        expected_key = hashlib.sha256(raw_string.encode()).hexdigest()
        if expected_key != license_key:
            return False
        if not is_license_valid_for_device(license_key):
            return False
        return True
    except (ValueError, IndexError):
        return False

# Fungsi untuk menghapus file lisensi
def delete_license_file():
    if os.path.exists('user_license.txt'):
        os.remove('user_license.txt')

# Fungsi untuk mendapatkan UUID acak sebagai Device ID
def get_device_id():
    return str(uuid.uuid4())

# Fungsi untuk memverifikasi apakah lisensi valid untuk perangkat saat ini
def is_license_valid_for_device(license_key):
    device_id = get_device_id()
    if os.path.exists('device_license.txt'):
        with open('device_license.txt', 'r') as file:
            for line in file:
                saved_license_key, saved_device_id = line.strip().split(',')
                if saved_license_key == license_key:
                    return saved_device_id == device_id
    return True

# Fungsi untuk menyimpan Device ID bersama dengan lisensi
def save_license_for_device(license_key):
    device_id = get_device_id()
    with open('device_license.txt', 'a') as file:
        file.write(f"{license_key},{device_id}\n")

# Fungsi untuk menghitung sisa waktu lisensi dalam hari
def get_license_days_left(license_key):
    try:
        _, expiration_timestamp = license_key.split('-')
        expiration_timestamp = int(expiration_timestamp)
        current_timestamp = datetime.datetime.now().timestamp()
        days_left = (expiration_timestamp - current_timestamp) / (60 * 60 * 24)
        return max(0, int(days_left))
    except (ValueError, IndexError):
        return 0

# Fungsi untuk menghasilkan barcode Code128
def generate_code128_barcode(text, barcode_size, output_dir):
    options = {
        'module_height': barcode_size,
        'module_width': 1,
        'quiet_zone': 15,
        'text_distance': 5,
        'font_size': 10,
        'background': 'white',
        'foreground': 'black'
    }

    code128 = barcode.get('code128', text, writer=ImageWriter())
    filename = os.path.join(output_dir, f'{text}.png')
    code128.save(filename, options)

    print(f"BARCODE UNTUK '{text}' BERHASIL DIBUAT DAN DISIMPAN SEBAGAI {filename}")

# Fungsi untuk mencetak teks secara perlahan
def print_slow(text):
    import sys, time
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def menu():
    blue_color = "\033[94m"
    green_color = "\033[92m"
    cyan_color = "\033[96m"
    red_color = "\033[91m"
    yellow_color = "\033[93m"
    magenta_color = "\033[95m"
    reset_color = "\033[0m"

    lines = [
        "  ____   ___  ____  ______   __  _ _____ ",
        " |  _ \\ / _ \\| __ )| __ ) \\ / / / |___ / ",
        " | |_) | | | |  _ \\|  _ \\\\ V /   | | |_ \\ ",
        " |  _ <| |_| | |_) | |_) || |   | |___) |",
        " |_| \\_\\___/|____/|____/ |_|    |_|____/ "
    ]

    print_slow(f"{blue_color} ╔════════════════════════════════════════╗{reset_color}")
    for line in lines:
        print_slow(f"{cyan_color} {line} {reset_color}")
    print_slow(f"{yellow_color}               IDM | {red_color}V2.2.0{reset_color}")
    print_slow(f"{blue_color} ╚════════════════════════════════════════╝{reset_color}")
    print()

    print(f"{yellow_color}   *** MENU SCRIPT INDOMARET ***{reset_color}")
    print(f"{yellow_color}-----------------------------------{reset_color}")
    
    # Menu items with icons
    menu_items = [
        "[1] 📝  GENERATE BARCODE",
        "[2] 📦  STOCK OPNAME (MAINTENANCE)",
        "[3] 🔑  MASA AKTIF LISENSI",
        "[4] ❌  EXIT"
    ]
    
    for item in menu_items:
        print(f"{green_color}{item}{reset_color}")
    
    # Footer
    print(f"{yellow_color}-----------------------------------{reset_color}")
    
    # User choice
    choice = input(f"{green_color}PILIH MENU: {reset_color}")
    return choice

# Fungsi untuk membaca PLU dari file
def read_plu_from_file(filename):
    plu_list = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            plu = line.strip()
            if plu:
                plu_list.append(plu)
    return plu_list

def main():
# Fungsi untuk menyimpan informasi lisensi
def save_license_info(user_id, license_key):
    with open('user_license.txt', 'w') as file:
        file.write(f"{user_id}\n{license_key}")

# Fungsi untuk memuat informasi lisensi
def load_license_info():
    if os.path.exists('user_license.txt'):
        with open('user_license.txt', 'r') as file:
            user_id = file.readline().strip()
            license_key = file.readline().strip()
            return user_id, license_key
    return None, None

# Fungsi untuk memanggil script kedua
def panggil_script_kedua():
    subprocess.run(["python", "so.py"])

# Fungsi utama
if __name__ == "__main__":
    clear_screen()

    user_id, license_key = load_license_info()

    if user_id is None or license_key is None:
        device_id = get_device_id()
        print(f"DEVICE ID ANDA: {device_id}")
        user_id = input(" USER ID : ")
        license_key = input(" LICENSE KEY : ")
        save_license_info(user_id, license_key)
        save_license_for_device(license_key)

    if verify_license(user_id, license_key):
        print("              LICENSE KEY VALID!.")
        try:
            while True:
                choice = menu()

                if choice == "1":
                    input_file = "input.txt"
                    barcode_size = float(input("MASUKKAN SIZE BARCODE (mm): "))
                    output_dir = "BARCODE"

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    plu_list = read_plu_from_file(input_file)

                    for plu in plu_list:
                        generate_code128_barcode(plu, barcode_size, output_dir)

                elif choice == "2":
                    panggil_script_kedua()

                elif choice == "3":
                    days_left = get_license_days_left(license_key)
                    print(f"MASA AKTIF LISENSI ANDA {days_left} HARI LAGI.")

                elif choice == "4":
                    print("Keluar...")
                    break

                else:
                    print("Pilihan tidak valid. Silakan masukkan 1, 2, 3, atau 4.")
        finally:
            # Tidak ada lagi pemanggilan unmark_license_in_use
            pass
    else:
        red_color = "\033[91m"
        reset_color = "\033[0m"
        print(f"{red_color}                   LICENSE KEY INVALID!!. ACCESS DENIED.{reset_color}")
        delete_license_file()
        print(" PLEASE CONTACT ADMIN https://wa.me/6285314247652 FOR YOUR LICENSE.")

if __name__ == "__main__":
    main()