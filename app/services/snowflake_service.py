# app/services/snowflake_service.py
from app.config import get_sf_connection

def get_schemas(database: str):
    conn = get_sf_connection(database)
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW SCHEMAS")
        result = cursor.fetchall()
        return [row[1] for row in result] 
    finally:
        cursor.close()
        conn.close()

# app/services/snowflake_service.py

def get_tables(database: str, schema: str):
    conn = get_sf_connection(database)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SHOW TABLES IN {database}.{schema}")
        result = cursor.fetchall()
        return [row[1] for row in result]  # table name is in column index 1
    finally:
        cursor.close()
        conn.close()

# app/services/snowflake_service.py

def get_columns(database: str, schema: str, table: str):
    conn = get_sf_connection(database)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DESC TABLE {database}.{schema}.{table}")
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Extract only name, type, comment
        return [
            {
                "name": row[0],
                "type": row[1],
                "description": row[6]  # index 6 is the COMMENT field
            }
            for row in result
        ]
    finally:
        cursor.close()
        conn.close()

# app/services/snowflake_service.py

def get_table_summary(database: str, schema: str, table: str):
    conn = get_sf_connection(database)
    cursor = conn.cursor()
    try:
        # Describe table to get column types
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
            return {"message": "No columns to summarize"}

        summary_query = f"""
            SELECT {', '.join(select_parts)}
            FROM {database}.{schema}.{table}
        """

        cursor.execute(summary_query)
        row = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]

        # Zip column names and values into a dict
        return dict(zip(columns, row))

    finally:
        cursor.close()
        conn.close()
