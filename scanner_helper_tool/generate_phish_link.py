"""
╔══════════════════════════════════════════════════════════════════╗
║      LIVE PHISHING DATASET GENERATOR — TECHNICAL CLASSIFIER      ║
║  Pembaruan: Mengklasifikasi vektor serangan secara otomatis      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import requests
import csv
import os
import re
from urllib.parse import urlparse

def duga_kategori_serangan(url):
    """
    Fungsi ini membedah anatomi URL untuk menentukan teknik manipulasi (Attack Vector)
    berdasarkan 15 Kategori Standar Pengujian.
    """
    url_lc = url.lower()
    
    # Memecah URL menjadi bagian-bagian (domain, path, dll)
    try:
        parsed = urlparse(url_lc)
        domain = parsed.netloc
        path = parsed.path
    except:
        domain = ""
        path = ""

    # 1. Data URIs
    if url_lc.startswith('data:'):
        return "Data URIs"

    # 2. Deep Links
    if url_lc.startswith(('intent:', 'market:', 'android-app:')):
        return "Deep Links"

    # 3. Punycode (IDN Encoding)
    if 'xn--' in domain:
        return "Punycode"

    # 4. IP-Based URLs (Mengecek apakah domain murni berupa angka IP)
    # Regex ini mencari pola seperti 192.168.1.1
    if re.search(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]+)?$", domain):
        return "IP-Based URLs"

    # 5. URL Shorteners
    shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly', 'rebrand.ly', 'cutt.ly', 'shorturl.at', 'short.link']
    if any(domain == s or domain.endswith('.' + s) for s in shorteners):
        return "URL Shorteners"

    # 6. Suspicious TLDs (Domain gratisan yang sering disalahgunakan)
    bad_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.online', '.site', '.icu', '.vip', '.pw']
    if any(domain.endswith(tld) for tld in bad_tlds):
        return "Suspicious TLDs"

    # 7. Excessive Subdomains
    # Menghitung jumlah titik di domain. Misal: login.secure.bca.co.id.baddomain.com (ada 6 titik)
    if domain.count('.') >= 4:
        return "Excessive Subdomains"

    # 8. Mixed Content / HTTP Manipulation
    # Mengecek apakah pakai HTTP biasa atau ada karakter '@' (Basic Auth Spoofing)
    if url_lc.startswith('http://') or '@' in url_lc:
        return "Mixed Content"

    # 9. Credential Harvesting (Pola paling umum di phishing)
    cred_keywords = ['login', 'signin', 'verify', 'account', 'secure', 'auth', 'update', 'recovery', 'confirm']
    if any(kw in path or kw in domain for kw in cred_keywords):
        return "Credential Harvesting"

    # 10. Fallback (Jika tidak masuk pola teknis di atas, ancaman dari OpenPhish biasanya berupa Typosquatting)
    return "Typosquatting"


def tarik_live_phishing(jumlah_target=30):
    url_sumber = "https://openphish.com/feed.txt"
    file_csv = "dataset(3).csv"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("📡 Menghubungi server OpenPhish...")
    
    try:
        respon = requests.get(url_sumber, headers=headers, timeout=10)
        
        if respon.status_code == 200:
            semua_link = respon.text.strip().split('\n')
            semua_link = [link for link in semua_link if link.strip() != ""]
            
            link_terpilih = semua_link[:jumlah_target]
            
            data_baru = []
            print("⚙️ Membedah anatomi URL dan mengklasifikasikan teknik serangan...")
            
            for link in link_terpilih:
                # Memanggil fungsi bedah URL di atas
                kategori_teknis = duga_kategori_serangan(link)
                data_baru.append([link, "phishing", kategori_teknis])
            
            file_exists = os.path.isfile(file_csv)
            with open(file_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['url', 'label', 'kategori'])
                writer.writerows(data_baru)
                
            print(f"✅ Sukses! {len(link_terpilih)} link berhasil diklasifikasikan dan disimpan.")
        else:
            print(f"❌ API OpenPhish memblokir akses. Kode Error: {respon.status_code}")
            
    except Exception as error:
        print(f"💥 Terjadi kesalahan: {error}")


# Jalankan fungsinya untuk 71 target (sesuai permintaan sebelumnya)
tarik_live_phishing(170)