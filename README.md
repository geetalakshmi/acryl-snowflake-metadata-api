# acryl-snowflake-metadata-api
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload 
uvicorn app.main:app --reload --log-level debug
