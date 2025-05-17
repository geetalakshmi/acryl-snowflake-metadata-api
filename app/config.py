# app/config.py
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def get_sf_connection(database=None):
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=database or os.getenv("SNOWFLAKE_DATABASE"),
    )
