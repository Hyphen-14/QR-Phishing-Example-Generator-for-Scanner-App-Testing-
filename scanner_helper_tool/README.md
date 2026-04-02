# 🛡️ QR Security Scanner Tester — Research Suite

Suite alat komprehensif untuk menguji keandalan aplikasi *Barcode/QR Scanner* pada perangkat seluler dalam mendeteksi ancaman *phishing* dan *malware*. Proyek ini mencakup script *generator* dataset ancaman nyata (*live feeds*) dan GUI aplikasi pengujian interaktif (Mendukung logging via Excel lokal & Google Sheets Cloud).

## 📋 Persyaratan Sistem
- Python 3.8+
- Library bawaan: `tkinter`, `csv`, `os`, `time`
- Library eksternal: `qrcode`, `pillow`, `openpyxl`, `requests`, `gspread`, `oauth2client`

## ⚙️ Instalasi

Buka terminal/Command Prompt dan jalankan perintah berikut untuk menginstal semua *dependencies* yang dibutuhkan:

```bash
pip install qrcode pillow openpyxl requests gspread oauth2client
```

## 🛠️ TAHAP 1: Generate Dataset Pengujian
Sebelum mulai melakukan scanning, siapkan data URL yang akan diuji. Anda bisa membuat file dataset.csv secara manual, atau menggunakan script generator otomatis yang telah disediakan. Script ini akan otomatis menambahkan data ke file dataset.csv.

**Jalankan script sesuai kebutuhan riset Anda:**

### Live Phishing (Ancaman Nyata) ☠️
Mengambil URL phishing yang sedang aktif dari database (PhishStats / OpenPhish).

```Bash
python phishstats_generator.py
```
### Industry Standard Testing 🛡️
Mengambil URL pengujian resmi yang diakui vendor antivirus global (AMTSO, EICAR, Google Safe Browsing).

```Bash
python industry_test_generator.py
```
### Live Safe URLs (Control Group) ✅
Mengambil URL aman secara acak dari Hacker News dan Wikipedia untuk menguji False Positive Rate.

```Bash
python live_safe_generator.py
```
## Format baku dataset.csv:

```Code snippet
url,label,kategori
[https://www.google.com](https://www.google.com),safe,Live Safe (Wikipedia)
[http://malware.testing.google.test/testing/malware/,phishing,Industry](http://malware.testing.google.test/testing/malware/,phishing,Industry) Standard (Google Safe)
```

## 🚀 TAHAP 2: Menjalankan Aplikasi Tester
Pilih salah satu versi aplikasi sesuai dengan alur kerja tim Anda:

**Opsi A: Versi Lokal (Log ke Excel)**
Cocok untuk pengujian mandiri tanpa koneksi internet yang stabil.

```Bash
python qr_scanner_tester.py
```
**Opsi B: Versi Cloud (Log Real-Time ke Google Sheets)**
Cocok untuk kolaborasi tim secara live. Semua hasil scan langsung terkirim ke Google Sheets.

```Bash
python qr_scanner_live.py
```
### ⚠️ Penting untuk Versi Cloud: > Pastikan Anda sudah memiliki file credentials.json (dari Google Cloud Console) di folder yang sama, dan sudah membagikan akses editor Google Sheets Anda ke email Service Account tersebut. Sesuaikan variabel SPREADSHEET_NAME di dalam script.

## 🖥️ Cara Penggunaan GUI
1. Load Dataset: Klik tombol "📂 Load Dataset CSV" untuk memuat daftar URL dari dataset.csv.

2. Atur Output Log:
```
(Versi Lokal): Klik "📄 Buat Excel Baru" untuk memulai file log dari awal, atau "📥 Buka Excel Lama" untuk melanjutkan pendataan ke file pekerjaan teman.
```

3. Pilih Scanner: Pada panel kanan, pilih nama HP/Scanner yang sedang Anda gunakan (contoh: iOS Camera).

4. Mulai Scan: Arahkan kamera HP ke QR Code yang tampil di layar laptop.

5. Catat Hasil (Penting): Klik tombol sesuai dengan respon dari HP Anda:
```
🚨 PHISHING TERDETEKSI: Jika HP menolak membuka link, menampilkan layar peringatan merah, atau memberi label berbahaya.

✅ AMAN / DIBUKA: Jika HP langsung membuka website tanpa peringatan apapun.

⚠️ TIDAK BISA SCAN: Jika kamera gagal membaca QR Code. (Data akan dilewati).
```
6. Ulangi untuk URL selanjutnya. Jangan lupa mengganti nama Scanner di dropdown jika Anda berganti perangkat penguji.

## ⌨️ Keyboard Shortcuts
Untuk mempercepat proses scanning tanpa harus menggunakan mouse:
| Tombol | Aksi |
|--------|------|
| 1 | Phishing Terdeteksi |
| 2 | Aman / Dibuka |
| 3 | Tidak bisa scan (Skip) |
| → | URL berikutnya |
| ← | URL sebelumnya |

## 📊 Membaca Hasil Output
Di dalam Excel / Google Sheets, Anda akan menemukan:

Sheet Per Scanner (Contoh: 'iOS Camera'): Berisi log row-by-row lengkap dengan status True Positive (TP), False Positive (FP), False Negative (FN), dan True Negative (TN).

Sheet 'Ringkasan' (Khusus Versi Lokal): Tabel perbandingan otomatis yang menghitung metrik performa tiap scanner, mencakup nilai Precision, Recall (Detection Rate), dan F1-Score.

## 🔄 Alur Pengujian Ideal (Best Practice)
Untuk mendapatkan metrik evaluasi yang reliable secara akademis:

Sesi 1: Uji seluruh dataset (Misal 150 URL) menggunakan iOS Camera (Built-in).

Sesi 2: Uji dataset yang persis sama menggunakan Android Camera.

Sesi 3: Uji dataset yang persis sama menggunakan aplikasi pihak ketiga (Google Lens / Lionic).

Analisis komparasi melalui sheet Ringkasan untuk melihat scanner mana yang memiliki Recall (tingkat deteksi ancaman) paling tinggi tanpa mengorbankan keamanan (False Positive yang rendah).