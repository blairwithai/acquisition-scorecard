# Acquisition Scorecard (Streamlit)

An interactive web app that turns your acquisition scorecard spreadsheet into a point-and-click tool.

## Why Streamlit?
- **Fast to ship**: paste `app.py`, deploy in minutes.
- **No heavy frontend**: sliders, tables, and downloads out-of-the-box.
- **Easy hosting**: Streamlit Cloud (free) or Replit (share a URL).

## Files
- `app.py` — the app
- `requirements.txt` — Python deps
- `data/TEMPLATE_Acquisition_Scorecard.xlsx` — your bundled example file
- `README.md` — this guide

Detected columns in your spreadsheet: ['Category', 'Item', 'Responsible Party for Assessment', 'Weight', 'Score (1-5)', 'Weighted Score', 'Out of ', 'Unnamed: 7', 'OVERALL SCORE', 60.30800000000006, 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'].

---

## Run Locally (fastest)
1. Install Python 3.10+
2. In a terminal:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Your browser opens at `http://localhost:8501`

## Deploy on Replit
1. Create a new **Python** Repl.
2. Upload all files/folders from this repo (including `/data`).
3. In the Replit "Shell", run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py --server.address=0.0.0.0 --server.port=8000
   ```
4. Open the webview; the app will be live.

> Tip: You can also set the Run command to:
> `streamlit run app.py --server.address=0.0.0.0 --server.port=8000`

## Deploy on Streamlit Community Cloud (free)
1. Push these files to a new GitHub repo.
2. Go to Streamlit Community Cloud → **Deploy an app**.
3. Select your repo & branch, set the file to `app.py`.
4. Click **Deploy**. Done — share the URL.

## How to Use
- Upload an XLSX/CSV with columns:
  - **Category**, **Item**, **Responsible Party for Assessment** (optional), **Weight**, **Score (1-5)**
- Edit values inline. The app calculates:
  - **Weighted Score per row** (= Weight × Score)
  - **Category scores (% of max points)**
  - **Overall score** (% of max points)
- Use **Exports** to download the summary or full table.

## Customize
- Toggle **Lock weights** in the sidebar to enforce consistency.
- Add **Notes** per line item for rationale.
- Extend columns or rename mappings in `app.py` (see `pick(...)`).

---

### Next steps (nice-to-have)
- Multi-deal comparison view
- Must-pass thresholds & auto flags
- PDF report export
- Save to Google Sheets/Airtable/Supabase
