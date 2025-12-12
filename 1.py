import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess 
import sys 

# --- Konfigurasi ---
KEY_FILE = 'watchful-lotus-480604-b6-fb4b1454eb7d.json' 
SHEET_NAME = 'SheetPY' 
WORKSHEET_NAME = 'Sheet1'
COLUMN_TO_CHECK = 'A'
# -------------------

def run_system_command(command: str):
    """Fungsi pembantu untuk menjalankan perintah sistem dan menangani error."""
    print("-" * 30)
    print(f"Executing system command: '{command}'")
    try:
        # Menjalankan perintah. shell=True digunakan untuk perintah shell.
        result = subprocess.run(command, shell=True, check=True)
        
        print(f"Perintah '{command}' selesai dieksekusi.")
    except subprocess.CalledProcessError as sub_e:
        print(f"🚨 ERROR: Perintah '{command}' gagal dengan return code {sub_e.returncode}")
        print("Cek output terminal Anda untuk detail kegagalan perintah sistem.")
    except FileNotFoundError:
        print(f"🚨 ERROR: Perintah '{command.split()[0]}' tidak ditemukan. Pastikan Anda berada di lingkungan yang benar (misal: Termux).")
    except Exception as sub_e:
        print(f"🚨 ERROR tak terduga saat menjalankan subprocess: {type(sub_e).__name__}: {sub_e}")
    print("-" * 30)


def check_google_sheet():
    # 1. Otentikasi
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scope)
        client = gspread.authorize(creds)

    except FileNotFoundError:
        print(f"Error: File '{KEY_FILE}' tidak ditemukan. Pastikan file kunci service account sudah ada.")
        return
    except Exception as e:
        print(f"Error saat otentikasi: {e}")
        return

    # 2. Membuka Google Sheet
    try:
        sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Google Sheet '{SHEET_NAME}' tidak ditemukan.")
        return
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Tab sheet '{WORKSHEET_NAME}' tidak ditemukan. Cek kembali nama tab.")
        return
    except Exception as e:
        print(f"Error saat membuka sheet: {e}")
        return

    # 3. Mendapatkan indeks kolom
    col_index = ord(COLUMN_TO_CHECK.upper()) - ord('A') + 1 

    # 4. Memuat nilai kolom HANYA SEKALI sebelum loop
    try:
        column_values = sheet.col_values(col_index)
        print(f"Data dari Kolom {COLUMN_TO_CHECK} berhasil dimuat.")
    except Exception as e:
        print(f"Error saat membaca data dari Google Sheet: {e}")
        return

    # 5. Loop untuk meminta input dan memverifikasi kunci
    while True:
        try:
            # a. Meminta input pengguna
            print("-" * 30)
            user_key = input("Masukan Product Key: ").strip()
            print("-" * 30)
            
            if not user_key:
                print("Product Key tidak boleh kosong. Coba lagi.")
                continue

            # b. Memeriksa kunci
            if user_key in column_values:
                print(f"Key Success ✅")
                
                # --- LOGIKA PENGHAPUSAN KUNCI ---
                try:
                    # Mencari indeks list (0-based) di mana kunci ditemukan.
                    list_index = column_values.index(user_key)
                    
                    # Indeks baris di Google Sheet (1-based) adalah (indeks list + 1)
                    row_to_delete = list_index + 1
                    
                    print(f"🔑 Key ditemukan di baris {row_to_delete}. Menghapus baris...")
                    
                    # ⚠️ Menghapus baris dari Google Sheet
                    sheet.delete_rows(row_to_delete)
                    
                    print("✅ Baris berisi Key berhasil dihapus dari Google Sheet.")
                    
                    # PERBAIKAN: Hapus elemen dari list lokal agar tidak perlu memuat ulang dari jaringan
                    del column_values[list_index]
                    
                except ValueError:
                    print("❌ Error internal: Kunci ditemukan di list tetapi gagal mendapatkan index.")
                except Exception as delete_e:
                    print(f"🚨 ERROR saat menghapus baris dari Google Sheet: {delete_e}")
                # ---------------------------------

                run_system_command('pkg install panji')
                break  # Kunci valid dan sudah diproses, keluar dari loop
            else:
                print(f" Key already used or not valid ❌")
                # Jalankan pkg update saat error
                run_system_command('pkg update')
                # Loop akan berulang
                
        except KeyboardInterrupt:
            # Menangkap Ctrl + C. Karena berada di dalam while True, 
            # ini hanya akan menghentikan input saat ini dan 
            # memulai iterasi loop berikutnya (kembali ke input key).
            print("\n\n⚠️ Ctrl+C Terdeteksi. Kembali ke input Product Key.")
            continue # Melanjutkan ke awal loop selanjutnya


if __name__ == "__main__":
    check_google_sheet()
