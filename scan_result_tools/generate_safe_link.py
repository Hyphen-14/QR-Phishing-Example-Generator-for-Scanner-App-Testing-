import csv
import random
import os

# 1. Siapkan bahan baku untuk di-mix (Domain aman)
kategori_aman = ["Education", "Tech & Developer", "Government", "News Portal", "E-Commerce"]
domain_utama = ["ui.ac.id", "itb.ac.id", "kemdikbud.go.id", "github.com", "stackoverflow.com", "tokopedia.com", "linux.org", "ubuntu.com", "detik.com", "kompas.com"]
subdomains = ["www", "blog", "news", "forum", "help", "docs", "portal", "secure", "career", "about"]

data_baru = []

# 2. Looping untuk bikin 120 link secara random
for i in range(120):
    kategori = random.choice(kategori_aman)
    domain = random.choice(domain_utama)
    sub = random.choice(subdomains)
    
    # Merakit URL
    url = f"https://{sub}.{domain}"
    
    # Memasukkan ke dalam list dengan format: [url, label, kategori]
    data_baru.append([url, "safe", kategori])

# 3. Target file
file_csv = "dataset.csv"

# 4. Mengecek apakah file dataset.csv sudah ada sebelumnya
file_exists = os.path.isfile(file_csv)

# 5. Membuka file dan menyuntikkan data
with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Kalau file belum ada, tulis header-nya dulu
    if not file_exists:
        writer.writerow(['url', 'label', 'kategori'])
        
    # Tulis semua 120 baris data ke dalam file
    writer.writerows(data_baru)

print("Berhasil menambahkan 120 link aman ke dataset.csv!")