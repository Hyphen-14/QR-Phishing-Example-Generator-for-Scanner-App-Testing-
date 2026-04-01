import requests
import csv
import os

def tarik_live_phishing(jumlah_target=30):
    url_sumber = "https://openphish.com/feed.txt"
    file_csv = "dataset.csv"
    
    # KUNCI RAHASIA: Menyamar sebagai browser Chrome di Windows 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("📡 Menghubungi server OpenPhish dengan penyamaran...")
    
    try:
        # Menambahkan headers ke dalam request
        respon = requests.get(url_sumber, headers=headers, timeout=10)
        
        if respon.status_code == 200:
            semua_link = respon.text.strip().split('\n')
            
            # Filter baris kosong supaya tidak error
            semua_link = [link for link in semua_link if link.strip() != ""]
            
            link_terpilih = semua_link[:jumlah_target]
            
            data_baru = []
            for link in link_terpilih:
                data_baru.append([link, "phishing", "Live Phishing (OpenPhish)"])
            
            file_exists = os.path.isfile(file_csv)
            with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['url', 'label', 'kategori'])
                writer.writerows(data_baru)
                
            print(f"✅ Sukses! {len(link_terpilih)} link berhasil disuntikkan ke {file_csv}")
        else:
            print(f"❌ Gagal. Server memblokir kita. Kode Error: {respon.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Error: Koneksi ke server OpenPhish terputus (Timeout/Kelamaan).")
    except Exception as error:
        print(f"💥 Terjadi kesalahan: {error}")

tarik_live_phishing(71)