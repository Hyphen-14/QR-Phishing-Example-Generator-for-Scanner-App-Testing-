"""
╔══════════════════════════════════════════════════════════════════╗
║      ROBOT GOOGLE LENS (ANTI-CAPTCHA EDITION) By Zeline          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import time
import csv
import datetime
import re
import random # Tambahan untuk jurus acak
import undetected_chromedriver as uc # Menggunakan versi stealth/penyamaran
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ─── BANTUAN EXCEL LOGGER (Sama seperti sebelumnya) ────
def thin_border():
    return Border(left=Side(style="thin"), right=Side(style="thin"), 
                  top=Side(style="thin"), bottom=Side(style="thin"))

class AutoExcelLogger:
    def __init__(self, path="QR_Scanner_Test_Log.xlsx"):
        self.path = path
        self.scanner_name = "Google Lens (Auto)"
        
        if os.path.exists(self.path):
            self.wb = load_workbook(self.path)
        else:
            from openpyxl import Workbook
            self.wb = Workbook()
            
        self._setup_sheet()

    def _setup_sheet(self):
        safe_name = self.scanner_name[:31]
        if safe_name not in self.wb.sheetnames:
            ws = self.wb.create_sheet(safe_name)
            headers = ["No", "Waktu", "URL", "Label Aktual", "Kategori", "Hasil Scanner", "TP", "FP", "FN", "TN", "Benar?", "Catatan Lens"]
            for col_idx, label in enumerate(headers, 1):
                cell = ws.cell(row=2, column=col_idx, value=label)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", start_color="1F3864")
            self.wb.save(self.path)

    def log_result(self, url, label, kategori, hasil_scanner, catatan=""):
        safe_name = self.scanner_name[:31]
        ws = self.wb[safe_name]
        row = ws.max_row + 1
        if row < 3: row = 3

        no = row - 2
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hasil_str = "Phishing" if hasil_scanner == "detected" else "Aman"

        tp = fp = fn = tn = 0
        if label == "phishing" and hasil_scanner == "detected": tp = 1; benar = "✅"
        elif label == "safe" and hasil_scanner == "detected": fp = 1; benar = "❌"
        elif label == "phishing" and hasil_scanner == "safe": fn = 1; benar = "❌"
        else: tn = 1; benar = "✅"

        bg = "E2EFDA" if benar == "✅" else "FFE0E0"
        data = [no, waktu, url, label, kategori, hasil_str, tp, fp, fn, tn, benar, catatan]
        
        for ci, val in enumerate(data, 1):
            cell = ws.cell(row=row, column=ci, value=val)
            cell.fill = PatternFill("solid", start_color=bg)
            cell.border = thin_border()

        self.wb.save(self.path)

# ─── FUNGSI BANTUAN: JEDA ACAK ───
def jeda_manusia(min_detik=2.0, max_detik=4.5):
    """Bikin jeda waktu acak biar Google nggak curiga ini robot"""
    waktu = random.uniform(min_detik, max_detik)
    time.sleep(waktu)

# ─── ROBOT OTOMASI SELENIUM ───────────────────────────────────────
def jalankan_robot():
    file_csv = "dataset.csv"
    folder_gambar = "qr_test_cases"
    
    if not os.path.exists(file_csv):
        print("❌ File dataset.csv tidak ditemukan!")
        return

    logger = AutoExcelLogger()
    print("✅ Excel Logger siap mencatat...")

    # Menggunakan Undetected Chromedriver agar lebih kebal blokir
    print("🤖 Menyalakan mesin Chrome Penyamaran (Stealth Mode)...")
    options = uc.ChromeOptions()
    options.add_argument('--lang=en')
    # Jangan pakai headless kalau lagi sering kena Captcha, biar kita bisa lihat dan bantu solve
    driver = uc.Chrome(options=options, version_main=146)
    driver.maximize_window()

    with open(file_csv, mode='r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        
    print(f"📂 Ditemukan {len(reader)} data untuk diuji.")

    try:
        for ri, row in enumerate(reader, 1):
            url_asli = row['url'].strip()
            label = row['label'].strip()
            kategori = row['kategori'].strip()
            
            file_safe_url = re.sub(r'[^a-zA-Z0-9]', '_', url_asli[:20])
            nama_file = f"qr_{ri:03}_{file_safe_url}.png"
            path_lengkap = os.path.abspath(os.path.join(folder_gambar, nama_file))
            
            if not os.path.exists(path_lengkap):
                print(f"   ⚠️ Lewati baris {ri}: Gambar {nama_file} tidak ditemukan.")
                continue

            print(f"\n🔍 [Scan {ri}/{len(reader)}] Sedang menguji: {url_asli}")
            
            driver.get('https://images.google.com/')
            jeda_manusia(1.5, 3.0) # Jeda acak sebelum klik
            
            # --- CEK CAPTCHA AWAL ---
            if "sorry" in driver.current_url or "captcha" in driver.page_source.lower():
                print("\n🚨🚨 WADUH! GOOGLE MENGELUARKAN CAPTCHA! 🚨🚨")
                print("Tolong selesaikan CAPTCHA di jendela Chrome secara manual.")
                input("👉 Tekan tombol ENTER di terminal ini KALAU CAPTCHA SUDAH BERES...")
                print("Lanjut bekerja...\n")
                driver.get('https://images.google.com/') # Refresh setelah captcha beres

            try:
                kamera = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, 'image') or contains(@aria-label, 'gambar')]"))
                )
                kamera.click()
                
                jeda_manusia(1.0, 2.0)
                
                upload_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
                )
                upload_input.send_keys(path_lengkap)
                
                # Tunggu Lens memproses gambar
                jeda_manusia(4.0, 6.0) 
                
                # --- CEK CAPTCHA SETELAH UPLOAD ---
                if "sorry" in driver.current_url or "captcha" in driver.page_source.lower():
                    print("\n🚨🚨 CAPTCHA MUNCUL PAS LAGI SCAN! 🚨🚨")
                    input("👉 Tolong selesaikan CAPTCHA di Chrome, lalu tekan ENTER di sini...")
                    jeda_manusia(2.0, 3.0)
                
                body_text = driver.find_element(By.TAG_NAME, "body").text
                url_clean = url_asli.replace("https://", "").replace("http://", "").split('/')[0]
                
                if url_clean in body_text:
                    hasil_scanner = "safe"
                    catatan = "QR terbaca normal oleh Lens."
                    print("   🟢 Hasil Lens: AMAN (Tembus)")
                else:
                    hasil_scanner = "detected"
                    catatan = "URL diblokir atau tidak dikenali."
                    print("   🔴 Hasil Lens: DIBLOKIR / TIDAK TERBACA")
                
                logger.log_result(url_asli, label, kategori, hasil_scanner, catatan)
                
            except Exception as e:
                print(f"   ⚠️ Error UI: Gagal menemukan tombol. Melewati URL ini...")
                logger.log_result(url_asli, label, kategori, "safe", f"Error Automasi.")
                
            jeda_manusia(2.0, 4.0) # Jeda acak sebelum pindah ke gambar berikutnya
            
    except KeyboardInterrupt:
        print("\n🛑 Dihentikan paksa oleh pengguna.")
    finally:
        print("\n🏁 Pengujian selesai. Menutup browser...")
        driver.quit()

jalankan_robot()