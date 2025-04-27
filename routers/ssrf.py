from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(prefix="/ssrf", tags=["ssrf"])

DEFAULT_URL = "https://www.opennet.ru/"

@router.get("/")
def fetch(url: str = DEFAULT_URL):
    """
    SSRF-vulnerable endpoint:
    - By default fetches DEFAULT_URL
    - If `url` is supplied, will fetch that URL unchecked
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        content = resp.text
        return {
            "fetched_url": url,
            "status_code": resp.status_code,
            "content_snippet": content[:512]
        }
    except requests.RequestException as exc:
        raise HTTPException(status_code=400, detail=f"Request failed: {exc}")
