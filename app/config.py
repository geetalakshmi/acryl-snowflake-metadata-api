import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import snowflake.connector

load_dotenv()

# === SQLAlchemy Engine (for SELECTs) ===
def get_sqlalchemy_engine(database=None):
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    role = os.getenv("SNOWFLAKE_ROLE")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    db = database or os.getenv("SNOWFLAKE_DATABASE")

    conn_str = (
        f"snowflake://{user}:{password}@{account}/{db}"
        f"?warehouse={warehouse}&role={role}"
    )

    return create_engine(conn_str)

# === Native Connector (for metadata) ===
def get_snowflake_connection(database=None):
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=database or os.getenv("SNOWFLAKE_DATABASE"),
    )
