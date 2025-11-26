import os
import oracledb
from dotenv import load_dotenv
load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_DSN = os.getenv("ORACLE_DSN")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

if not (ORACLE_USER and ORACLE_DSN and ORACLE_PASSWORD):
    raise EnvironmentError("Variables ORACLE_USER / ORACLE_DSN / ORACLE_PASSWORD no configuradas.")

# Ajuste: autonative vs thick driver dependendiente (si tienes clientes Oracle)
# oracledb.init_oracle_client(lib_dir="/path/to/instantclient") #uncomment si usas thick

def get_connection():
    """Devuelve una conexion a la DB. Usar con context manager."""
    conn = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
        encoding="UTF-8"
    )
    return conn

def fetch_all(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            cols = [d[0].lower() for d in cur.description] if cur.description else []
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            return rows
        
def execute(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            conn.commit()
            return cur.rowcount