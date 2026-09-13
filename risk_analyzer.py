risky_keywords = ["malware", "phishing", "hack", "crack", "torrent"]

def check_risky_sites(url):
    for word in risky_keywords:
        if word in url.lower():
            return True
    return False
