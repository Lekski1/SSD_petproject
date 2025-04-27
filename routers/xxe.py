from fastapi import APIRouter, UploadFile, HTTPException
from lxml import etree
from io import BytesIO

router = APIRouter(prefix="/xxe", tags=["xxe"])

@router.post("/")
async def parse_xml(file: UploadFile):
    try:
        contents = await file.read()
        parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)        
        root = etree.fromstring(contents, parser)
        result = []
        
        for child in root:
            result.append({child.tag: child.text})
            
        return {"status": "success", "data": result}
    
    except etree.XMLSyntaxError as e:
        raise HTTPException(status_code=400, detail=f"XML syntax error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {e}")
