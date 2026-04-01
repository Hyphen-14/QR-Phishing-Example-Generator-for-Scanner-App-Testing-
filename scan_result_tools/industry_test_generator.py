import csv
import os

def tambah_standar_industri():
    file_csv = "dataset.csv"
    
    # Kumpulan link resmi untuk pengujian keamanan
    # Link ini disepakati oleh vendor antivirus sedunia (Google, Kaspersky, dll)
    link_industri = [
        # AMTSO (Anti-Malware Testing Standards Organization)
        ["https://desktop.amtso.org/check-desktop-phishing-page/", "phishing", "Industry Standard (AMTSO)"],
        ["https://desktop.amtso.org/check-desktop-download-test/", "phishing", "Industry Standard (AMTSO Malware)"],
        ["https://desktop.amtso.org/check-desktop-pup-test/", "phishing", "Industry Standard (AMTSO PUP)"],
        
        # Google Safe Browsing Test
        ["http://malware.testing.google.test/testing/malware/", "phishing", "Industry Standard (Google Safe)"],
        
        # WICAR (Web-based EICAR Test)
        ["http://wicar.org/test-malware.html", "phishing", "Industry Standard (WICAR)"],
        ["http://www.eicar.org/download/eicar.com", "phishing", "Industry Standard (EICAR)"],
        
        # PhishTank Test Page (Halaman khusus yang selalu dilabeli phishing)
        ["http://www.phishtank.com/phish_detail.php?phish_id=1", "phishing", "Industry Standard (PhishTank)"]
    ]
    
    print("Mempersiapkan link standar uji industri...")
    
    # Mengecek dan menulis ke CSV
    file_exists = os.path.isfile(file_csv)
    with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Bikin header kalau file belum ada
        if not file_exists:
            writer.writerow(['url', 'label', 'kategori'])
            
        # Tulis semua data industri ke CSV
        writer.writerows(link_industri)
        
    print(f"✅ Sukses! {len(link_industri)} link pengujian standar industri berhasil disuntikkan ke {file_csv}")

# Menjalankan fungsi
tambah_standar_industri()