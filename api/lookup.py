import json
import requests
from http.server import BaseHTTPRequestHandler
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        key = query_params.get('key', [None])[0]
        query = query_params.get('query', [None])[0]

        # 1. Custom API Key check
        if key != "DEMO":
            self.send_response(401)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid API Key"}, ensure_ascii=False).encode('utf-8'))
            return

        if not query:
            self.send_response(400)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'query' parameter"}, ensure_ascii=False).encode('utf-8'))
            return

        try:
            # 2. Real API call
            real_url = f"https://telegram2num.noobster11001.workers.dev/fast?key=noobster&q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            response = requests.get(real_url, headers=headers, timeout=15)
            real_data = response.json()

            # 3. Check data
            if not real_data.get("status") or "tg_id" not in real_data:
                self.send_response(404)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": False, 
                    "message": "No data found for this Telegram ID."
                }, ensure_ascii=False).encode('utf-8'))
                return

            # 4. Extract data
            tg_id = real_data.get("tg_id", "N/A")
            phone_list = real_data.get("phone", [])
            
            if phone_list and len(phone_list) > 0:
                phone_info = phone_list[0]
                phone_number = phone_info.get("number", "N/A")
                country_code = phone_info.get("country_code", "N/A")
                country_name = phone_info.get("country", "N/A")
            else:
                phone_number = "N/A"
                country_code = "N/A"
                country_name = "N/A"

            # 5. Aapka custom format
            custom_response = (
                f"🆔 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 • {tg_id}\n"
                f"📞 𝗣𝗵𝗼𝗻𝗲 • {phone_number}\n"
                f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 • {country_name}\n"
                f"📡 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲 • {country_code}\n\n"
                f"├ 🛠️ ᴅᴇᴠᴇʟᴏᴘᴇʀ: ᴀᴋᴀꜱʜ ᴏꜱɪɴᴛ • 🛰️"
            )

            # 6. JSON Response (Bot ke liye)
            # ensure_ascii=False ka matlab hai emojis ko \ud83c mein convert mat karo
            response_data = {
                "status": True,
                "response": custom_response
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": False, "message": "Internal Server Error"}, ensure_ascii=False).encode('utf-8'))
