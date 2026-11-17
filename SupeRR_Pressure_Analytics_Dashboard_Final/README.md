# SupeRR Selector Pressure Analytics Dashboard

## Run on Windows (PowerShell)

Open PowerShell in this folder and run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python` is not recognised, use the Python launcher:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Do **not** launch this app with `python app.py`. Streamlit apps must be launched with `streamlit run` (or `python -m streamlit run`).

## Publish a shareable dashboard link

1. Create a GitHub repository.
2. Upload `app.py`, `analysis.xlsx`, and `requirements.txt`.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select the repository, branch, and `app.py` as the main file.
5. Deploy and copy the resulting `*.streamlit.app` URL into the Unstop dashboard-link field.

## Data handling

The dashboard uses aggregate player statistics from the supporting analysis workbook. Do not upload the original proprietary raw competition data pack to a public repository. Check the competition's data-sharing terms before publishing any derived player-level data.
