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
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Invalid API Key".encode('utf-8'))
            return

        if not query:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing 'query' parameter".encode('utf-8'))
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
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("No data found for this Telegram ID.".encode('utf-8'))
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

            # 5. Aapka custom format (Direct emojis)
            custom_response = (
                f"🆔 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 • {tg_id}\n"
                f"📞 𝗣𝗵𝗼𝗻𝗲 • {phone_number}\n"
                f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 • {country_name}\n"
                f"📡 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲 • {country_code}\n\n"
                f"├ 🛠️ ᴅᴇᴠᴇʟᴏᴘᴇʀ: ᴀᴋᴀꜱʜ ᴏꜱɪɴᴛ • 🛰️"
            )

            # 6. Direct Plain Text Response (No JSON)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(custom_response.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(custom_response.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
