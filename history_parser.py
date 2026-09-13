import sqlite3
from risk_analyzer import check_risky_sites

def parse_history(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM urls")
    rows = cursor.fetchall()

    risky_sites = []
    for row in rows:
        url = row[0]
        if check_risky_sites(url):
            risky_sites.append(url)

    conn.close()
    return risky_sites
