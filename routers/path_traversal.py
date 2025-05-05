import os

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter(prefix="/path_traversal", tags=["path traversal attack"])

# Define a base directory for files
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "files")

# Create the directory if it doesn't exist
os.makedirs(BASE_DIR, exist_ok=True)

# Create some sample files
sample_files = {
    "public_info.txt": "This is a public information file that anyone can access.",
    "user_data.txt": "User data: John (admin), Alice (user), Bob (user)",
    "secret.txt": "Secret key: kj23h4kj2h3k4jh23kj4h"
}

for filename, content in sample_files.items():
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(content)

@router.get("/", response_class=HTMLResponse)
def file_browser():
    """
    This endpoint shows a file browser interface with a Path Traversal vulnerability.
    """
    # List files in the base directory
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    
    file_list = "\n".join([f'<li><a href="/path_traversal/view?file={f}">{f}</a></li>' for f in files])
    
    html_content = f"""
    <html>
        <head>
            <title>File Browser</title>
        </head>
        <body>
            <h1>File Browser</h1>
            <p>Click on a file to view its contents:</p>
            
            <ul>
                {file_list}
            </ul>
            
            <h2>View Custom File</h2>
            <form action="/path_traversal/view" method="GET">
                <label for="file">File name:</label>
                <input type="text" id="file" name="file" placeholder="Enter filename" required><br><br>
                
                <input type="submit" value="View File">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/view")
async def view_file(file: str = Query(...)):
    """
    This endpoint is vulnerable to Path Traversal attacks because it doesn't properly
    validate or sanitize the file parameter, allowing access to files outside the intended directory.
    """
    # Vulnerable implementation: directly joining paths without validation
    file_path = os.path.join(BASE_DIR, file)
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read and return file content
        with open(file_path, 'r') as f:
            content = f.read()
            
        return PlainTextResponse(content=content)
    except Exception as e:
        if "File not found" in str(e):
            raise e
        return PlainTextResponse(content=f"Error: {str(e)}", status_code=500)

@router.get("/attack", response_class=HTMLResponse)
def path_traversal_attack_page():
    """
    This page demonstrates how to perform a Path Traversal attack.
    """
    attack_html = """
    <html>
        <head>
            <title>Path Traversal Demo</title>
        </head>
        <body>
            <h1>Path Traversal Attack Demonstration</h1>
            <p>This page shows how an attacker could access files outside the intended directory.</p>
            
            <h2>Examples of Path Traversal Attacks:</h2>
            <ul>
                <li><a href="/path_traversal/view?file=../../../etc/passwd" target="_blank">Try to access /etc/passwd</a></li>
                <li><a href="/path_traversal/view?file=..%2F..%2F..%2Fetc%2Fpasswd" target="_blank">URL encoded: Try to access /etc/passwd</a></li>
                <li><a href="/path_traversal/view?file=../../../etc/hosts" target="_blank">Try to access /etc/hosts</a></li>
                <li><a href="/path_traversal/view?file=../routers/path_traversal.py" target="_blank">Try to access this code file</a></li>
            </ul>
            
            <h2>What is Path Traversal?</h2>
            <p>Path traversal (also known as directory traversal) attacks aim to access files and directories that are stored outside the intended directory. 
            By using "../" sequences and their variations, attackers can navigate the directory structure to access sensitive files.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=attack_html)
