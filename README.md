# 🌍 Geo Minigames (Streamlit)

A lightweight Streamlit app with a starter **Guess the Flag** minigame.

## Quickstart

```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt
brew install redis
brew services start redis
mkdir .streamlit
touch .streamlit/secrets.toml
touch .env # (add export ENV=redis-local)
source .env

# 3) Run the app
streamlit run app.py
```

The sidebar will show available minigames (pages).
