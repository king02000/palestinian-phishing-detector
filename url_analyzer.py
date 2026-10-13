import re
from urllib.parse import urlparse

def extract_url_features(url: str) -> dict:
    if not url or url == "N/A":
        return {
            "url_length": 0,
            "has_ip": 0,
            "num_dots": 0,
            "has_suspicious_keywords": 0,
            "is_https": 0
        }
    
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    
    # فحص وجود عنوان IP في الرابط
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    has_ip = 1 if re.match(ip_pattern, hostname) else 0
    
    # الكلمات المفتاحية الشائعة في روابط التصيد
    keywords = ["login", "verify", "secure", "account", "bank", "free", "update", "claim"]
    has_keywords = 1 if any(kw in url.lower() for kw in keywords) else 0
    
    return {
        "url_length": len(url),
        "has_ip": has_ip,
        "num_dots": url.count('.'),
        "has_suspicious_keywords": has_keywords,
        "is_https": 1 if parsed.scheme == "https" else 0
    }