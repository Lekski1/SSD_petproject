from fastapi import APIRouter, HTTPException
from database import get_db_connection
import time

router = APIRouter(prefix="/ddos", tags=["ddos attack"])

@router.get("/")
def long_endpoint():
    """
    This endpoint is intentionally slow to be vulnerable to DDoS attacks.
    """
    # Create large list to consume memory
    large_list = [i for i in range(10000000)]
    time.sleep(2)
    return "Ok!"
