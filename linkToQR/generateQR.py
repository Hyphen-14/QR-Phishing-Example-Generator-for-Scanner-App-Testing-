import csv
import qrcode
import os
import re

def konversi_csv_ke_qr(file_input="dataset(2).csv"):
    # Nama folder output untuk menyimpan gambar
    folder_output = "qr_test_cases(2)"
    file_dataset = "dataset(2).csv"

    # Buat folder output kalau belum ada
    if not os.path.exists(folder_output):
      os.makedirs(folder_output)
      print(f"📁 Membuat folder baru: '{folder_output}'")
    else:
        print(f"📁 Folder output '{folder_output}' sudah ada.")

    if not os.path.exists(file_dataset):
        print(f"❌ Error: File '{file_dataset}' tidak ditemukan. Jalankan script generator dulu!")
        return

    print(f"📄 Membaca dataset dari '{file_dataset}'...")
    counter = 0
    
    # Membuka CSV dalam mode baca
    with open(file_input, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Mengecek apakah kolom 'url' ada
        if 'url' not in reader.fieldnames:
            print("❌ Error: Kolom 'url' tidak ditemukan di dataset.csv!")
            return

        # Looping per baris data
        for ri, row in enumerate(reader, 1):
            link = row['url'].strip()
            
            # Abaikan baris kosong
            if not link:
                continue

            # Setup QR Code Generator
            qr = qrcode.QRCode(
                version=1,                           # Ukuran dasar
                error_correction=qrcode.constants.ERROR_CORRECT_H, # Koreksi kesalahan tertinggi (bagus buat kamera HP)
                box_size=10,                         # Ukuran pixel
                border=4,                            # Ukuran border putih
            )
            
            qr.add_data(link)
            qr.make(fit=True)
            
            # Membuat gambar QR (warna hitam putih standar)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Menyiapkan nama file gambar
            # Agar file tertata, kita pakai nomor urut dan hapus karakter aneh dari URL
            file_safe_url = re.sub(r'[^a-zA-Z0-9]', '_', link[:20]) # Ambil 20 karakter depan aja
            file_name = f"qr_{ri:03}_{file_safe_url}.png"              # Misal: qr_001_https___google.com.png
            path_lengkap = os.path.join(folder_output, file_name)
            
            # Menyimpan gambar
            img.save(path_lengkap)
            
            if ri % 5 == 0:
                print(f"   ⚙️ Berhasil mengonversi baris {ri}...")
            counter += 1

    print(f"\n✅ Sukses! Total {counter} gambar QR Code tersimpan di folder '{folder_output}'.")

# Menjalankan fungsi
konversi_csv_ke_qr()