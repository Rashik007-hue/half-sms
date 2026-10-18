import json
import urllib.parse
import urllib.request
import ssl

# Owner Info
OWNER = "@RASHIK_69"

def handler(request):
    # Vercel থেকে কোয়েরি প্যারামিটার নেওয়া
    query = urllib.parse.parse_qs(request.args)
    
    num = query.get("num", [""])[0]
    name = query.get("name", [""])[0]
    msg = query.get("msg", [""])[0]

    # ভ্যালিডেশন
    if not num or not name or not msg:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps({
                "owner": OWNER,
                "status": False,
                "error": "Missing parameters. Required: num, name, msg"
            }, ensure_ascii=False, indent=4)
        }

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

    # SSL ভেরিফিকেশন ডিজেবল করা (আপনার আগের কোডের মতো)
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
                json_data["owner"] = OWNER # Owner অ্যাড করা হলো
                body = json.dumps(json_data, ensure_ascii=False, indent=4)
            except json.JSONDecodeError:
                body = json.dumps({
                    "owner": OWNER,
                    "status": True,
                    "raw_response": res_body
                }, ensure_ascii=False, indent=4)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json; charset=utf-8"},
                "body": body
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps({
                "owner": OWNER,
                "status": False,
                "error": f"Request Error: {str(e)}"
            }, ensure_ascii=False, indent=4)
        }
