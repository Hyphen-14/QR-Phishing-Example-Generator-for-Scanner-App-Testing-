import requests
import csv
import os
import time

def tarik_link_aman_live(jumlah_target_tech=30):
    file_csv = "dataset.csv"
    data_baru = []

    print("📡 1. Mengambil link Tech aktif dari Hacker News...")
    try:
        # Mengambil daftar ID artikel yang lagi ngetren hari ini
        url_hn = "https://hacker-news.firebaseio.com/v0/topstories.json"
        respon_hn = requests.get(url_hn, timeout=10)
        
        # respon_hn.json() akan mengubah data dari internet jadi format List di Python
        # [:jumlah_target_tech] membatasi agar kita tidak narik semua (ratusan) datanya
        id_artikel = respon_hn.json()[:jumlah_target_tech] 

        # Melakukan looping untuk mengecek isi masing-masing artikel
        for item_id in id_artikel:
            url_detail = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            respon_detail = requests.get(url_detail, timeout=5)
            detail = respon_detail.json()

            # Mengecek apakah artikel ini punya URL (karena kadang ada yang cuma teks diskusi)
            if 'url' in detail:
                link_asli = detail['url']
                data_baru.append([link_asli, "safe", "Live Safe (Tech News)"])

            # time.sleep(0.1) memberikan jeda 0.1 detik sebelum request berikutnya
            # Ini etika programming (Rate Limiting) agar server tidak menganggap kita spam
            time.sleep(0.1)

        print(f"✅ Dapat {len(data_baru)} link Tech asli yang lagi aktif!")

    except Exception as e:
        print(f"❌ Gagal ambil dari Hacker News: {e}")

    print("\n📡 2. Mengambil link random dari Wikipedia Indonesia...")
    try:
        url_wiki = "https://id.wikipedia.org/api/rest_v1/page/random/summary"
        link_wiki_terkumpul = 0

        # Looping terus sampai kita dapat 20 link Wikipedia
        while link_wiki_terkumpul < 20:
            respon_wiki = requests.get(url_wiki, timeout=5)
            
            # Kalau respon dari server adalah 200 (OK/Sukses)
            if respon_wiki.status_code == 200:
                data_wiki = respon_wiki.json()
                
                # Menyelusup ke dalam data JSON untuk mengambil URL aslinya
                link_asli = data_wiki['content_urls']['desktop']['page']
                data_baru.append([link_asli, "safe", "Live Safe (Wikipedia)"])
                
                link_wiki_terkumpul += 1 # Menambah hitungan
                
            time.sleep(0.1) # Jeda sopan santun ke server

        print(f"✅ Dapat 20 link Wikipedia asli!")

    except Exception as e:
        print(f"❌ Gagal ambil dari Wikipedia: {e}")

    # ─── MENYIMPAN KE DATASET.CSV ───
    if data_baru:
        file_exists = os.path.isfile(file_csv)
        
        # Buka file CSV dengan mode 'a' (append) agar menambah di baris bawah
        with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Kalau file dataset.csv kebetulan belum ada, buatkan baris judul (header)
            if not file_exists:
                writer.writerow(['url', 'label', 'kategori'])
                
            # Tulis semua data yang sudah dikumpulkan sekaligus
            writer.writerows(data_baru)

        print(f"\n🎉 Sukses menyuntikkan total {len(data_baru)} link aman (LIVE) ke {file_csv}")
    else:
        print("⚠ Wah, sepertinya tidak ada data yang berhasil ditarik.")

# Jalankan fungsinya
tarik_link_aman_live(30)