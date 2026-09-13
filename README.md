Browser History Analyzer

This project analyzes browser history and identifies risky websites.
It now runs as a browser-based UI so you can use it from your web browser instead of the terminal.

Features:
- Parse browser history
- Identify risky sites
- Show most visited sites
- View results in a clean HTML interface

Setup:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the web app:
   ```bash
   python main.py
   ```
3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```
4. Enter the full path to your Chrome `History` file and submit.

Files added:
- `templates/index.html` — browser UI form and result page
- `static/styles.css` — page styling for UI
- `requirements.txt` — Flask dependency
