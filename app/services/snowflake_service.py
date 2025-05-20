# app/services/snowflake_service.py
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, OperationalError, DatabaseError
from app.config import get_snowflake_connection
from cachetools import cached, TTLCache
from app.utils.logger import setup_logger
logger = setup_logger()

# Cache results for 10 minutes (600 seconds)
cache = TTLCache(maxsize=100, ttl=600)

@cached(cache)
def get_schemas(database: str):
    try:
        logger.info(f"Fetching schemas for database: {database}")
        conn = get_snowflake_connection(database)
        cursor = conn.cursor()
        try:
            cursor.execute("SHOW SCHEMAS")
            result = cursor.fetchall()
            return [row[1] for row in result]  # schema name at index 1
        finally:
            cursor.close()
            conn.close()

    except ProgrammingError:
        raise ValueError(f"Invalid database name '{database}' or access denied.")

    except OperationalError:
        raise ValueError("Unable to connect to Snowflake. Check credentials or network.")

    except DatabaseError as e:
        raise ValueError(f"Snowflake database error: {str(e)}")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

# app/services/snowflake_service.py
@cached(cache)
def get_tables(database: str, schema: str):
    try:
        logger.info(f"Fetching tables for {database}.{schema}")
        conn = get_snowflake_connection(database)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SHOW TABLES IN {database}.{schema}")
            result = cursor.fetchall()
            return [row[1] for row in result]  # table name is in column index 1
        finally:
            cursor.close()
            conn.close()

    except ProgrammingError:
        raise ValueError(f"Invalid schema '{schema}' in database '{database}', or access denied.")

    except OperationalError:
        raise ValueError("Unable to connect to Snowflake. Check credentials or network.")

    except DatabaseError as e:
        raise ValueError(f"Snowflake database error while listing tables: {str(e)}")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

# app/services/snowflake_service.py
@cached(cache)
def get_columns(database: str, schema: str, table: str):
    try:
        logger.info(f"Fetching columns for {database}.{schema}.{table}")
        conn = get_snowflake_connection(database)
        cursor = conn.cursor()
        try:
            query = f"DESC TABLE {database}.{schema}.{table}"
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [
                {
                    "name": row[0],
                    "type": row[1],
                    "description": row[6] or "—"  # comment is at index 6
                }
                for row in result
            ]
        finally:
            cursor.close()
            conn.close()

    except ProgrammingError:
        raise ValueError(f"Invalid table '{table}' in schema '{schema}' or access denied.")

    except OperationalError:
        raise ValueError("Unable to connect to Snowflake. Check credentials or network.")

    except DatabaseError as e:
        raise ValueError(f"Snowflake error while describing table: {str(e)}")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

# app/services/snowflake_service.py
def get_table_summary(database: str, schema: str, table: str):
    try:
        logger.info(f"Fetching summary for {database}.{schema}.{table}")
        conn = get_snowflake_connection(database)
        cursor = conn.cursor()
        try:
            # Step 1: Get column types
            cursor.execute(f"DESC TABLE {database}.{schema}.{table}")
            desc_result = cursor.fetchall()

            numeric_cols = []
            text_cols = []

            for row in desc_result:
                col_name = row[0]
                col_type = row[1].upper()
                if "NUMBER" in col_type or "INT" in col_type or "FLOAT" in col_type:
                    numeric_cols.append(col_name)
                else:
                    text_cols.append(col_name)

            # Step 2: Build aggregation query
            select_parts = []

            for col in numeric_cols:
                select_parts.extend([
                    f"COUNT({col}) AS {col}_count",
                    f"MIN({col}) AS {col}_min",
                    f"MAX({col}) AS {col}_max",
                    f"AVG({col}) AS {col}_avg"
                ])

            for col in text_cols:
                select_parts.extend([
                    f"COUNT({col}) AS {col}_count",
                    f"COUNT(DISTINCT {col}) AS {col}_unique"
                ])

            if not select_parts:
                return {"message": "No columns to summarize."}

            # Step 3: Run summary query
            summary_query = f"""
                SELECT {', '.join(select_parts)}
                FROM {database}.{schema}.{table}
            """

            cursor.execute(summary_query)
            row = cursor.fetchone()
            columns = [desc[0] for desc in cursor.description]

            return dict(zip(columns, row))

        finally:
            cursor.close()
            conn.close()

    except ProgrammingError:
        raise ValueError(f"Table '{table}' not found in schema '{schema}' or access denied.")

    except OperationalError:
        raise ValueError("Could not connect to Snowflake. Please check your credentials or network.")

    except SQLAlchemyError as e:
        raise ValueError(f"Snowflake error while generating summary: {str(e)}")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")
