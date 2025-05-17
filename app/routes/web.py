# app/routes/web.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.snowflake_service import get_schemas
from fastapi.templating import Jinja2Templates
from app.services.snowflake_service import get_tables
from app.services.snowflake_service import get_columns
from app.services.snowflake_service import get_table_summary

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/schemas/{database}", response_class=HTMLResponse)
def list_schemas(request: Request, database: str):
    try:
        schemas = get_schemas(database)
        return templates.TemplateResponse("schemas.html", {"request": request, "schemas": schemas, "database": database})
    except Exception as e:
        return templates.TemplateResponse("schemas.html", {"request": request, "schemas": [], "database": database, "error": str(e)})

@router.get("/schemas", response_class=HTMLResponse)
def list_schemas_query(request: Request, database: str):
    return list_schemas(request, database)

# app/routes/web.py



@router.get("/tables/{database}/{schema}", response_class=HTMLResponse)
def list_tables(request: Request, database: str, schema: str):
    try:
        tables = get_tables(database, schema)
        return templates.TemplateResponse("tables.html", {
            "request": request,
            "tables": tables,
            "database": database,
            "schema": schema
        })
    except Exception as e:
        return templates.TemplateResponse("tables.html", {
            "request": request,
            "tables": [],
            "database": database,
            "schema": schema,
            "error": str(e)
        })



@router.get("/columns/{database}/{schema}/{table}", response_class=HTMLResponse)
def list_columns(request: Request, database: str, schema: str, table: str):
    try:
        columns = get_columns(database, schema, table)
        return templates.TemplateResponse("columns.html", {
            "request": request,
            "columns": columns,
            "database": database,
            "schema": schema,
            "table": table
        })
    except Exception as e:
        return templates.TemplateResponse("columns.html", {
            "request": request,
            "columns": [],
            "database": database,
            "schema": schema,
            "table": table,
            "error": str(e)
        })

# app/routes/web.py



@router.get("/summary/{database}/{schema}/{table}", response_class=HTMLResponse)
def summary_view(request: Request, database: str, schema: str, table: str):
    try:
        stats = get_table_summary(database, schema, table)
        return templates.TemplateResponse("summary.html", {
            "request": request,
            "summary": stats,
            "database": database,
            "schema": schema,
            "table": table
        })
    except Exception as e:
        return templates.TemplateResponse("summary.html", {
            "request": request,
            "summary": None,
            "error": str(e),
            "database": database,
            "schema": schema,
            "table": table
        })
