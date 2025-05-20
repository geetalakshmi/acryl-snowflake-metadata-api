# app/tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_schemas_html():
    response = client.get("/schemas/LONG_TAIL_COMPANIONS")
    assert response.status_code == 200
    assert "<table" in response.text

def test_invalid_schema():
    response = client.get("/schemas/INVALID_DB")
    assert response.status_code in [404, 500]

# Tables
def test_list_tables_html():
    response = client.get("/tables/LONG_TAIL_COMPANIONS/ECOMMERCE")
    assert response.status_code == 200
    assert "<li" in response.text or "<table" in response.text

def test_invalid_table_schema():
    response = client.get("/tables/LONG_TAIL_COMPANIONS/FAKE_SCHEMA")
    assert response.status_code in [404, 500]

# Columns
def test_list_columns():
    response = client.get("/columns/LONG_TAIL_COMPANIONS/ECOMMERCE/LINEITEM")
    assert response.status_code == 200
    assert "Name" in response.text and "Type" in response.text

def test_invalid_column_table():
    response = client.get("/columns/LONG_TAIL_COMPANIONS/ECOMMERCE/FAKE_TABLE")
    assert response.status_code in [404, 500]

# Summary
def test_summary_valid():
    response = client.get("/summary/LONG_TAIL_COMPANIONS/ECOMMERCE/LINEITEM")
    assert response.status_code == 200
    assert "Summary" in response.text or "<table" in response.text

def test_summary_invalid():
    response = client.get("/summary/LONG_TAIL_COMPANIONS/ECOMMERCE/FAKE_TABLE")
    assert response.status_code in [404, 500]