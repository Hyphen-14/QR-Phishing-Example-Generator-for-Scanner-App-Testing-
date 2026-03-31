# QR Security Scanner Tester — Panduan Instalasi & Penggunaan

## 📋 Persyaratan
- Python 3.8+
- Library: qrcode, pillow, openpyxl, tkinter (bawaan Python)

## ⚙️ Instalasi

```bash
pip install qrcode pillow openpyxl
```

## 🚀 Cara Menjalankan

```bash
python qr_scanner_tester.py
```

## 📁 Format Dataset CSV

Siapkan file CSV dengan kolom berikut:

```
url,label,kategori
https://google.com,safe,Search Engine
http://phishing-site.xyz,phishing,Fake Banking
```

- **url** : URL yang akan diuji
- **label** : `safe` atau `phishing` (label aktual/kebenaran)
- **kategori** : deskripsi singkat (opsional, untuk pelaporan)

## 🖥️ Cara Penggunaan

1. **Buka app** → jalankan `python qr_scanner_tester.py`
2. **Load Dataset** → klik tombol "📂 Load Dataset CSV"
3. **Pilih Output Excel** → klik "💾 Pilih File Excel Output"
4. **Pilih Scanner** → pilih HP/scanner yang sedang diuji dari dropdown
5. **Scan QR** → arahkan HP ke QR yang muncul di layar
6. **Catat hasil** → klik tombol sesuai respons HP:
   - 🚨 **Phishing Terdeteksi** → HP memberi peringatan/memblokir
   - ✅ **Aman / Tidak ada peringatan** → HP langsung membuka URL
   - ⚠️ **Tidak bisa scan** → QR tidak terbaca, dilewati
7. **Ganti scanner** → ubah dropdown, ulangi dari langkah 5

## ⌨️ Keyboard Shortcuts

| Tombol | Aksi |
|--------|------|
| `1` | Phishing Terdeteksi |
| `2` | Aman |
| `3` | Tidak bisa scan |
| `→` | URL berikutnya |
| `←` | URL sebelumnya |

## 📊 Output Excel

File Excel akan memiliki sheet:
- **[Nama Scanner]** — log detail per scanner (TP/FP/FN/TN per URL)
- **Ringkasan** — perbandingan metrik semua scanner (Precision, Recall, F1-Score)

## 🔄 Alur Pengujian Ideal

```
Sesi 1: Uji semua URL dengan iOS Camera
  ↓
Sesi 2: Uji semua URL yang sama dengan Android Camera
  ↓
Sesi 3: Uji semua URL yang sama dengan Google Lens
  ↓
Lihat Ringkasan → bandingkan metrik antar scanner
```

Ulangi minimal 3 sesi untuk hasil yang konsisten dan reliable.
