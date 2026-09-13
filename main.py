import os
import shutil
import tempfile
import sqlite3
from flask import Flask, render_template, request
from history_parser import parse_history

app = Flask(__name__)

def find_default_history():
    candidates = [
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History"),
        os.path.expanduser("~/.config/google-chrome/Default/History"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return ""

def get_top_sites(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "url": row[0],
            "title": row[1] or "No title",
            "visits": row[2]
        }
        for row in rows
    ]

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    top_sites = []
    risky_sites = []
    default_path = find_default_history()
    db_path = default_path if request.method == "GET" else ""

    if request.method == "POST":
        db_path = request.form.get("db_path", "").strip()
        expanded_path = os.path.expanduser(db_path)

        if not db_path:
            error = "Please enter the full path to your Chrome History file."
        elif not os.path.exists(expanded_path):
            error = f"History file not found: {db_path}"
        else:
            temp_db = None
            try:
                # Copy to temp file to prevent "database is locked" error if Chrome is running
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
                temp_db = tmp.name
                tmp.close()
                shutil.copy2(expanded_path, temp_db)

                top_sites = get_top_sites(temp_db)
                risky_sites = parse_history(temp_db)
            except Exception as exc:
                error = f"Error reading history file: {exc}"
            finally:
                if temp_db and os.path.exists(temp_db):
                    try:
                        os.remove(temp_db)
                    except OSError:
                        pass

    return render_template(
        "index.html",
        error=error,
        top_sites=top_sites,
        risky_sites=risky_sites,
        db_path=db_path or default_path,
    )

if __name__ == "__main__":
    import socket
    port = int(os.environ.get("PORT", 0))
    if not port:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", 5000))
            s.close()
            port = 5000
        except OSError:
            port = 5001
    print(f"Starting server on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)

