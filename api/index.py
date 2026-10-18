from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import urllib.request
import ssl

OWNER = "@RASHIK_69"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api")
@app.get("/api/index")
async def root(num: str = "", name: str = "", msg: str = ""):
    if not num or not name or not msg:
        return {
            "owner": OWNER,
            "status": True,
            "message": "CarryBee API is live",
            "usage": "?num=01XXXXXXXXX&name=YourName&msg=BusinessName"
        }

    payload = {"name": name, "phone_number": num, "business_name": msg}
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2027 Build/SP1A.210812.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.43 Mobile Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "origin": "https://merchant.carrybee.com",
        "referer": "https://merchant.carrybee.com/",
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        "https://api-merchant.carrybee.com/api/v2/merchant/register",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            body = r.read().decode("utf-8")
            try:
                data = json.loads(body)
                data["owner"] = OWNER
                return data
            except json.JSONDecodeError:
                return {"owner": OWNER, "status": True, "raw_response": body}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"owner": OWNER, "status": False, "error": str(e)},
        )
