import json
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # URL se parameters nikaalein
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        key = query_params.get('key', [None])[0]
        query = query_params.get('query', [None])[0]

        # 1. Custom API Key check
        if key != "DEMO":
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid API Key"}).encode())
            return

        # 2. Query check
        if not query:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'query' parameter"}).encode())
            return

        try:
            # 3. Real API call (urllib use karke)
            real_url = f"https://telegram2num.noobster11001.workers.dev/fast?key=noobster&q={query}"
            
            req = urllib.request.Request(real_url)
            with urllib.request.urlopen(req, timeout=15) as response:
                real_data = json.loads(response.read().decode())

            # 4. Check karein data mila ya nahi
            if not real_data.get("status") or "tg_id" not in real_data:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": False, 
                    "message": "No data found for this Telegram ID."
                }).encode())
                return

            # 5. Data extract karein
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

            # 6. Aapka custom format (Extra data hidden)
            custom_response = (
                f"🆔 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 • {tg_id}\n"
                f"📞 𝗣𝗵𝗼𝗻𝗲 • {phone_number}\n"
                f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 • {country_name}\n"
                f"📡 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲 • {country_code}\n\n"
                f"├ 🛠️ ᴅᴇᴠᴇʟᴏᴘᴇʀ: ᴀᴋᴀꜱʜ ᴏꜱɪɴᴛ • 🛰️"
            )

            # 7. Response bhejein
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": True,
                "response": custom_response
            }).encode())

        except Exception:
            # Koi bhi error aaye toh real API ka URL hide rahega
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": False, 
                "message": "Internal Server Error"
            }).encode())
