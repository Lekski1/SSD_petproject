from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/sql_injection", tags=["sql injection"])

@router.get("/")
def search_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    vuln_query = f'SELECT * FROM users WHERE username = "{username}"'
    rows = cursor.execute(vuln_query).fetchall()
    conn.close()
    return {"sql injection": rows}