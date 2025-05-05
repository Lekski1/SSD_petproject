from fastapi import APIRouter, HTTPException
from starlette.responses import HTMLResponse
import requests

router = APIRouter(prefix="/xss", tags=["xss"])

@router.get("/")
def human_information(first_name: str, last_name: str):
    """
    XSS-vulnerable endpoint. Shows HTML page with user inputted data.
    """

    html = f"""
    <html>
        <body>
            <p>Kind: human</p>
            <p>First name: {first_name}</p>
            <p>Last name: {last_name}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
