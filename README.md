# ❄️ Acryl Snowflake Metadata Explorer (Custom UI)

This project is a lightweight FastAPI + Jinja2 web application to explore metadata from a Snowflake data warehouse. It supports schema, table, and column discovery along with summary statistics — all displayed in a clean, custom web UI (no Swagger).

---

## 🚀 Features

- 🔍 View all schemas in a Snowflake database
- 📂 Explore tables by schema
- 🧱 Inspect table columns (name, type, description)
- 📊 View summary statistics for each table (count, min, max, avg, uniqueness)
- 💻 FastAPI with Jinja2 (Bootstrap-styled UI)
- ⚙️ Hybrid engine using:
  - `snowflake-connector-python` for metadata queries (SHOW/DESC)
  - `SQLAlchemy` for SELECT queries
- 🧪 Unit-tested routes with `pytest`
- ♻️ Caching, error handling, and logging built-in

---

## 📦 Requirements

- Python 3.8+
- A valid Snowflake account and credentials

---

## 🔧 Setup Instructions

### 1 Clone the repo
```bash
git clone https://github.com/your-username/acryl-snowflake-metadata-api.git
cd acryl-snowflake-metadata-api
```
### 2 Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```
### 3 Install dependencies
```bash
pip install -r requirements.txt
```
### 4 Create a .env file with Snowflake credentials
```bash
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
```
### 5 Run the App
```bash
uvicorn app.main:app --reload
http://127.0.0.1:8000
```
### 6 Running Tests
```bash
pytest tests/ -v
```

### 7 Folder Structure
```bash
acryl-snowflake-metadata-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   └── utils/
├── tests/
├── .env
├── requirements.txt
└── README.md
```