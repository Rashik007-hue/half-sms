from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import urllib.parse
import urllib.request
import ssl

# Owner Info
OWNER = "@RASHIK_69"

app = FastAPI()

# CORS যাতে যেকোনো জায়গা থেকে কল করা যায়
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "owner": OWNER,
        "status": True,
        "message": "CarryBee API is Live",
        "usage": "/?num=01XXXXXXXXX&name=YourName&msg=YourBusiness"
    }

@app.get("/api/register")
async def register(num: str = "", name: str = "", msg: str = ""):
    # ভ্যালিডেশন
    if not num or not name or not msg:
        raise HTTPException(
            status_code=400, 
            detail={
                "owner": OWNER,
                "status": False, 
                "error": "Missing parameters. Required: num, name, msg"
            }
        )

    payload = {
        "name": name,
        "phone_number": num,
        "business_name": msg
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2027 Build/SP1A.210812.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.43 Mobile Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "origin": "https://merchant.carrybee.com",
        "referer": "https://merchant.carrybee.com/",
        "accept-language": "en-US,en;q=0.9",
    }

    # SSL ভেরিফিকেশন ডিজেবল
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        "https://api-merchant.carrybee.com/api/v2/merchant/register",
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            res_body = response.read().decode('utf-8')
            try:
                json_data = json.loads(res_body)
                json_data["owner"] = OWNER
                return json_data
            except json.JSONDecodeError:
                return {
                    "owner": OWNER,
                    "status": True,
                    "raw_response": res_body
                }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "owner": OWNER,
                "status": False,
                "error": f"Request Error: {str(e)}"
            }
        )
