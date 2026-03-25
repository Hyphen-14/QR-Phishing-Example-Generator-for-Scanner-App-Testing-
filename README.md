# QR Phishing Test Suite Generator

> **Academic Research Tool** untuk menguji keamanan aplikasi barcode scanner terhadap serangan phishing via QR code.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Cara Kerja Aplikasi Barcode Scanner](#cara-kerja-aplikasi-barcode-scanner)
3. [Struktur Test Cases](#struktur-test-cases)
4. [Cara Penggunaan](#cara-penggunaan)
5. [Mekanisme Deteksi QR Phishing](#mekanisme-deteksi-qr-phishing)
6. [Analisis Hasil Testing](#analisis-hasil-testing)
7. [Referensi](#referensi)

---

## Overview

Script ini menghasilkan **285 QR test cases** yang mencakup berbagai teknik phishing untuk menguji sejauh mana aplikasi barcode scanner dapat mendeteksi dan melindungi pengguna dari ancaman QR phishing.

### Kategori Test Cases

| Kategori | Jumlah | Risk Level | Deskripsi |
|----------|--------|------------|-----------|
| **Legitimate URLs** | 20 | Low | URL legitim untuk control group |
| **URL Shorteners** | 30 | Medium | URL shortener yang bisa disalahgunakan |
| **Homograph Attacks** | 25 | Critical | Unicode look-alike characters |
| **IP-Based URLs** | 20 | High | URL berbasis IP address |
| **Suspicious TLDs** | 25 | High | Top-level domains mencurigakan |
| **Typosquatting** | 30 | Critical | Common misspellings dari brand |
| **Data URIs** | 15 | Critical | Embedded content berbahaya |
| **Deep Links** | 15 | High | Intent URLs dan deep links |
| **Mixed Content** | 15 | High | HTTP URLs dengan manipulasi |
| **Excessive Subdomains** | 15 | High | Terlalu banyak subdomain |
| **Special Characters** | 15 | High | Karakter spesial dalam domain |
| **Zero-Width Characters** | 10 | Critical | Invisible Unicode characters |
| **Punycode** | 15 | Critical | IDN encoding untuk spoofing |
| **Redirect Chains** | 15 | Medium | URL shortener chains |
| **Credential Harvesting** | 20 | Critical | Fake login pages |

**Total: 285 test cases**

---

## Cara Kerja Aplikasi Barcode Scanner

### 1. **QR Code Decoding Process**

```
┌─────────────────┐
│  Camera Feed    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Image Processing │ → Deteksi QR code dalam frame
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ QR Decoding     │ → Ekstrak data dari QR (URL/text)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ URL Analysis    │ → Analisis URL yang diekstrak
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Security Check  │ → Deteksi phishing/malicious
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Action     │ → Warning/Block/Open URL
└─────────────────┘
```

### 2. **Komponen Utama dalam Aplikasi Scanner**

#### A. **QR Decoder Library**
- **ZXing** (Zebra Crossing) - Library paling umum
- **ML Kit** (Google) - Vision-based decoding
- **ZBar** - Alternative decoder
- **BoofCV** - Computer vision library

```java
// Contoh penggunaan ZXing
MultiFormatReader reader = new MultiFormatReader();
Result result = reader.decode(bitmap);
String qrContent = result.getText();
```

#### B. **URL Parser & Validator**
```java
// Ekstrak komponen URL
URL url = new URL(qrContent);
String protocol = url.getProtocol();  // http atau https
String host = url.getHost();          // domain
String path = url.getPath();          // path
int port = url.getPort();             // port
```

#### C. **Security Analyzer**
Komponen ini yang paling penting untuk deteksi phishing:

---

## Mekanisme Deteksi QR Phishing

### **Layer 1: Pattern Matching (Static Analysis)**

Aplikasi scanner memeriksa URL terhadap pola-pola yang diketahui berbahaya:

```java
// Contoh implementasi pattern matching
public class PhishingDetector {

    // 1. IP-based URL detection
    private boolean isIpBasedUrl(String url) {
        String ipPattern = "^http://\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}";
        return url.matches(ipPattern);
    }

    // 2. Suspicious TLD detection
    private boolean hasSuspiciousTld(String url) {
        String[] suspiciousTlds = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz"};
        for (String tld : suspiciousTlds) {
            if (url.contains(tld)) return true;
        }
        return false;
    }

    // 3. Typosquatting detection (Levenshtein distance)
    private boolean isTyposquatting(String domain, String[] brands) {
        for (String brand : brands) {
            int distance = calculateLevenshteinDistance(domain, brand);
            if (distance > 0 && distance <= 2) return true;
        }
        return false;
    }

    // 4. Excessive subdomain detection
    private boolean hasExcessiveSubdomains(String url) {
        String host = extractHost(url);
        int subdomainCount = host.split("\\.").length - 2;  // minus domain dan TLD
        return subdomainCount > 3;
    }

    // 5. URL shortener detection
    private boolean isUrlShortener(String url) {
        String[] shorteners = {"bit.ly", "tinyurl.com", "t.co", "goo.gl"};
        for (String shortener : shorteners) {
            if (url.contains(shortener)) return true;
        }
        return false;
    }
}
```

### **Layer 2: Domain Reputation Check**

```java
public class DomainReputationChecker {

    // A. Local blacklist/whitelist
    private Set<String> blacklist = loadBlacklist();
    private Set<String> whitelist = loadWhitelist();

    public ReputationResult checkDomain(String domain) {
        if (whitelist.contains(domain)) {
            return ReputationResult.SAFE;
        }
        if (blacklist.contains(domain)) {
            return ReputationResult.KNOWN_MALICIOUS;
        }
        return ReputationResult.UNKNOWN;
    }

    // B. Google Safe Browsing API
    public SafeBrowsingResult checkWithGoogleSafeBrowsing(String url) {
        // API call ke Google Safe Browsing
        // Returns: SAFE, PHISHING, MALWARE, UNWANTED_SOFTWARE
    }

    // C. Real-time threat intelligence
    public ThreatIntelResult checkThreatIntelligence(String domain) {
        // Query ke threat intelligence feeds
        // PhishTank, OpenPhish, VirusTotal, etc.
    }
}
```

### **Layer 3: Heuristic Analysis**

```java
public class HeuristicAnalyzer {

    // 1. Homograph attack detection (IDN spoofing)
    public boolean detectHomographAttack(String domain) {
        // Periksa karakter Unicode yang mencurigakan
        // Contoh: Cyrillic 'о' (U+043E) vs Latin 'o' (U+006F)

        for (char c : domain.toCharArray()) {
            if (isSuspiciousUnicode(c)) {
                return true;
            }
        }
        return false;
    }

    // 2. Visual similarity analysis
    public double calculateVisualSimilarity(String domain1, String domain2) {
        // Gunakan algoritma seperti:
        // - Levenshtein distance
        // - Jaro-Winkler distance
        // - Cosine similarity pada character n-grams

        return similarityScore;
    }

    // 3. Entropy analysis (random domain detection)
    public double calculateDomainEntropy(String domain) {
        // Domain dengan entropy tinggi kemungkinan DGA (Domain Generation Algorithm)
        // Contoh: xk9m2pql7v.com

        return entropy;
    }

    // 4. Age of domain check
    public boolean isNewDomain(String domain) {
        // Domain yang baru didaftarkan (< 30 hari) lebih mencurigakan
        WhoisInfo whois = queryWhois(domain);
        return whois.getAgeInDays() < 30;
    }
}
```

### **Layer 4: Machine Learning Detection**

```python
# Contoh model ML untuk deteksi phishing
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer

class PhishingMLModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

    def extract_features(self, url):
        features = {
            'url_length': len(url),
            'num_dots': url.count('.'),
            'num_hyphens': url.count('-'),
            'num_slashes': url.count('/'),
            'has_ip': self.has_ip_address(url),
            'has_at_symbol': '@' in url,
            'has_double_slash': '//' in url.replace('https://', ''),
            'domain_entropy': self.calculate_entropy(url),
            'suspicious_words': self.count_suspicious_words(url),
            'is_https': url.startswith('https'),
        }
        return features

    def predict(self, url):
        features = self.extract_features(url)
        prediction = self.model.predict([features])
        return prediction[0]  # 0 = safe, 1 = phishing
```

### **Layer 5: Behavioral Analysis**

```java
public class BehavioralAnalyzer {

    // 1. Redirect chain analysis
    public RedirectAnalysis analyzeRedirects(String url, int maxRedirects) {
        List<String> redirectChain = new ArrayList<>();
        String currentUrl = url;
        int redirectCount = 0;

        while (redirectCount < maxRedirects) {
            HttpResponse response = makeRequest(currentUrl);

            if (response.isRedirect()) {
                redirectChain.add(currentUrl);
                currentUrl = response.getRedirectLocation();
                redirectCount++;
            } else {
                break;
            }
        }

        return new RedirectAnalysis(redirectChain, redirectCount);
    }

    // 2. Content analysis (jika app fetch preview)
    public ContentAnalysis analyzePageContent(String url) {
        // Fetch page content
        String html = fetchHtml(url);

        // Check for:
        // - Login forms
        // - Password fields
        // - Brand impersonation
        // - Suspicious scripts

        return new ContentAnalysis(
            hasLoginForm(html),
            hasPasswordField(html),
            detectedBrands(html),
            suspiciousScripts(html)
        );
    }

    // 3. SSL/TLS certificate validation
    public CertificateValidation validateCertificate(String url) {
        SSLContext sslContext = SSLContext.getInstance("TLS");
        // Check certificate validity, issuer, SAN, etc.

        return new CertificateValidation(
            isValid(),
            getIssuer(),
            getSubjectAlternativeNames(),
            getValidityPeriod()
        );
    }
}
```

---

## Struktur Test Cases

```
qr_test_cases/
├── images/                          # 285 QR code images
│   ├── QR_0001_legit_1.png
│   ├── QR_0002_legit_2.png
│   ├── QR_0021_short_1.png
│   └── ... (285 files)
│
├── data/                            # Metadata dan hasil
│   ├── test_cases_metadata.json     # Metadata lengkap
│   ├── test_cases_metadata.csv      # Format spreadsheet
│   └── generation_report.txt        # Summary report
│
├── generate_qr_tests.py             # Script utama generator
├── testing_helper.py                # Helper untuk mencatat hasil
└── README.md                        # Dokumentasi ini
```

---

## Cara Penggunaan

### 1. **Generate QR Test Cases**

```bash
# Install dependencies
pip install qrcode[pil]

# Jalankan generator
python generate_qr_tests.py
```

Output:
- 285 QR images di folder `images/`
- Metadata di folder `data/`

### 2. **Testing dengan Aplikasi Scanner**

#### Manual Testing:
1. Buka aplikasi barcode scanner
2. Scan QR code satu per satu
3. Catat perilaku aplikasi untuk setiap QR:
   - Apakah terdeteksi sebagai phishing?
   - Apakah warning ditampilkan?
   - Apakah user bisa proceed ke URL?

#### Automated Testing (dengan emulator):
```python
# Gunakan Appium untuk automated testing
from appium import webdriver

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    'appPackage': 'com.lionic.scanner',
    'appActivity': '.MainActivity'
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Simulate QR scan (inject image atau gunakan camera simulation)
```

### 3. **Mencatat Hasil Testing**

Gunakan `testing_helper.py`:

```python
from testing_helper import QRTestingHelper

helper = QRTestingHelper("data/test_cases_metadata.json")

# Catat hasil untuk setiap test
helper.record_test(
    case_id="QR_0001",
    detected_as_phishing=False,
    warning_shown=False,
    user_can_proceed=True,
    notes="Legitimate URL, correctly allowed"
)

helper.record_test(
    case_id="QR_0046",
    detected_as_phishing=True,
    warning_shown=True,
    user_can_proceed=False,
    notes="Homograph attack correctly blocked"
)

# Generate report
helper.generate_test_report("Lionic Scanner")
```

### 4. **Analisis Hasil**

Report akan menghasilkan:
- **Detection Rate**: % URL phishing yang terdeteksi
- **False Positive Rate**: % URL legitim yang salah terdeteksi
- **Block Rate**: % URL yang berhasil diblokir
- **Category Performance**: Performa per kategori serangan

---

## Analisis Hasil Testing

### Metrik Evaluasi

```
┌─────────────────────────────────────────────────────────────┐
│                    CONFUSION MATRIX                         │
├─────────────────┬─────────────────┬─────────────────────────┤
│                 │ Actual Phishing │ Actual Safe             │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Predicted       │ True Positive   │ False Positive          │
│ Phishing        │ (Correctly      │ (Safe URL flagged)      │
│                 │ blocked)        │                         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Predicted       │ False Negative  │ True Negative           │
│ Safe            │ (Phishing       │ (Safe URL allowed)      │
│                 │ allowed)        │                         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### Formula Metrik

```
Precision = TP / (TP + FP)
Recall (Sensitivity) = TP / (TP + FN)
Specificity = TN / (TN + FP)
F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Interpretasi Hasil

| Metrik | Target | Interpretasi |
|--------|--------|--------------|
| **Detection Rate** | > 90% | Seberapa baik app mendeteksi phishing |
| **False Positive Rate** | < 5% | Seberapa sering app salah flag URL legitim |
| **Block Rate** | > 85% | Seberapa efektif app mencegah akses |
| **Critical Miss Rate** | < 1% | Seberapa sering phishing kritis lolos |

---

## Teknik Evasi yang Diuji

### 1. **Homograph Attacks (IDN Spoofing)**

**Cara kerja:**
- Gunakan karakter Unicode yang terlihat identik dengan ASCII
- Contoh: Cyrillic 'о' (U+043E) vs Latin 'o' (U+006F)

**Ekspektasi:**
- App harus mendeteksi dan decode punycode
- Warning harus ditampilkan untuk IDN domains

**Contoh:**
```
Visual:    gооgle.com  (terlihat seperti google.com)
Actual:    gооgle.com  (Cyrillic o)
Punycode:  xn--ggle-wmc.com
```

### 2. **Zero-Width Characters**

**Cara kerja:**
- Sisipkan karakter invisible dalam URL
- Zero-width space (U+200B), zero-width joiner (U+200D)

**Ekspektasi:**
- App harus strip atau detect zero-width characters
- URL dengan zero-width chars harus dianggap suspicious

### 3. **Typosquatting**

**Cara kerja:**
- Registrasi domain dengan typo umum dari brand terkenal
- Contoh: paypa1.com, gooogle.com

**Ekspektasi:**
- App harus check similarity dengan brand terkenal
- Gunakan Levenshtein distance atau visual similarity

### 4. **URL Shorteners**

**Cara kerja:**
- Masking destination URL dengan shortener
- User tidak tahu kemana akan diarahkan

**Ekspektasi:**
- Warning untuk URL shortener
- Ideally: expand URL dan check destination

### 5. **Data URIs**

**Cara kerja:**
- Embed HTML/JavaScript langsung dalam QR
- Bisa berisi fake login form atau XSS

**Ekspektasi:**
- Block atau warning untuk data URIs
- Jangan langsung render content

---

## Referensi

### Academic Papers
1. **"QR Code Security: A Survey of Attacks and Challenges"** - IEEE 2020
2. **"Phishing Detection Using Machine Learning Techniques"** - ACM 2019
3. **"Visual Phishing: The Next Generation of Phishing Attacks"** - USENIX 2021

### Threat Intelligence Feeds
- [PhishTank](https://phishtank.org/)
- [OpenPhish](https://openphish.com/)
- [Google Safe Browsing](https://safebrowsing.google.com/)
- [VirusTotal](https://www.virustotal.com/)

### Tools
- **ZXing**: https://github.com/zxing/zxing
- **ML Kit**: https://developers.google.com/ml-kit
- **Appium**: https://appium.io/ (for automated testing)

### Standards
- **IDN (Internationalized Domain Names)**: RFC 3490-3492
- **Punycode**: RFC 3492
- **QR Code Specification**: ISO/IEC 18004

---

## Disclaimer

⚠️ **This tool is for academic research purposes only.**

- Gunakan hanya untuk menguji aplikasi yang Anda miliki atau miliki izin untuk diuji
- Jangan gunakan untuk aktivitas ilegal atau merusak
- Bertanggung jawab dalam melaporkan vulnerability ke developer

---

## License

MIT License - Academic Use

---

**Generated**: 2026-03-25  
**Version**: 1.0  
**Author**: Research Assistant
