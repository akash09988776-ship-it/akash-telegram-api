from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import json
import re
import os

# ---------- CONFIGURATION ----------
# ⚠️ Real API URL yahan hide hai (Response mein nahi jayega)
REAL_API_URL = os.getenv("TG_API_URL", "https://telegram2num.noobster11001.workers.dev/fast")
REAL_API_KEY = os.getenv("TG_API_KEY", "noobster")
DEVELOPER = "𐙚 𓆩𝘼𝙠𝙖𝙨𝗵 𝙊𝙨𝙞𝙣𝙩𓆪𓂂🧑‍💻🎀⃤"

# हमारी नई API का Key
API_KEY = "DEMO"
# नया गुप्त रास्ता
SECRET_PATH = "/v1/tg-lookup-z9x7q2m"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        key = params.get("key", [None])[0]
        raw_num = params.get("query", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # 1. URL चेक
        if parsed.path != SECRET_PATH:
            self.wfile.write(json.dumps({"status": False, "error": "Invalid Key"}, indent=4).encode())
            return

        # 2. API Key चेक
        if key != API_KEY:
            self.wfile.write(json.dumps({"status": False, "error": "Invalid Key"}, indent=4).encode())
            return

        # 3. Query चेक
        if not raw_num:
            self.wfile.write(json.dumps({"status": False, "error": "Invalid Key"}, indent=4).encode())
            return

        tg_id = re.sub(r"[^\d]", "", raw_num.strip())
        if not tg_id:
            self.wfile.write(json.dumps({"status": False, "error": "No data found"}, indent=4).encode())
            return

        # ---------- REAL API कॉल ----------
        try:
            # Aapke real API ka format (&q= query ke liye)
            real_url = f"{REAL_API_URL}?key={REAL_API_KEY}&q={tg_id}"
            req = urllib.request.Request(real_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw_text = resp.read().decode("utf-8", errors="ignore")
        except Exception:
            self.wfile.write(json.dumps({"status": False, "error": "No data found"}, indent=4).encode())
            return

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            self.wfile.write(json.dumps({"status": False, "error": "No data found"}, indent=4).encode())
            return

        # Parse Response
        result = self.parse_response(data, tg_id)
        
        if "error" in result and not result.get("Telegram ID"):
            self.wfile.write(json.dumps(result, indent=4, ensure_ascii=False).encode())
            return

        # 🔥 Aapka Custom Emoji Format
        custom_text = (
            f"🆔 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 • {result.get('Telegram ID')}\n"
            f"📞 𝗣𝗵𝗼𝗻𝗲 • {result.get('Phone')}\n"
            f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 • {result.get('Country')}\n"
            f"📡 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲 • {result.get('Country Code')}\n\n"
            f"├ 🛠️ ᴅᴇᴠᴇʟᴏᴘᴇʀ: {DEVELOPER} • 🛰️"
        )

        # Bot aur User dono ke liye Final Response
        final_response = {
            "status": True,
            "success": True,
            "response": custom_text,       # Aapka emoji format
            "Telegram ID": result.get('Telegram ID'),
            "Phone": result.get('Phone'),
            "Country": result.get('Country'),
            "Country Code": result.get('Country Code'),
            "developer": DEVELOPER
        }

        self.wfile.write(json.dumps(final_response, indent=4, ensure_ascii=False).encode())

    def parse_response(self, data, query):
        if not isinstance(data, dict):
            return {"error": "No data found"}

        status = data.get("status", "error")
        inner = data.get("data", {})

        if status != "success" or not inner:
            if "Phone" in data or "phone" in data or "tg_id" in data:
                inner = data
                status = "success"
            else:
                return {"status": False, "error": "No data found"}

        phone = (inner.get("Owner≠Number") or inner.get("Owner\u2260Number")
                 or inner.get("Phone") or inner.get("phone")
                 or inner.get("number") or inner.get("Number"))

        tg_id = (inner.get("TG -ID") or inner.get("TG-ID") or inner.get("TG ID")
                 or inner.get("Telegram ID") or inner.get("tg_id") or query)

        country_code = (inner.get("Country-Code") or inner.get("Country Code")
                        or inner.get("country_code"))
        country = inner.get("Country") or inner.get("country")

        if not phone:
            return {"status": False, "error": "No data found"}

        # Aapka diya hua Country Code Map
        country_map = {
            "+91": "India", "+880": "Bangladesh", "+92": "Pakistan",
            "+1": "United States/Canada", "+44": "United Kingdom",
            "+971": "United Arab Emirates", "+966": "Saudi Arabia",
            "+977": "Nepal", "+94": "Sri Lanka", "+60": "Malaysia",
            "+62": "Indonesia", "+63": "Philippines", "+84": "Vietnam",
            "+66": "Thailand", "+65": "Singapore", "+81": "Japan",
            "+82": "South Korea", "+86": "China", "+90": "Turkey",
            "+20": "Egypt", "+27": "South Africa", "+30": "Greece",
            "+31": "Netherlands", "+32": "Belgium", "+33": "France",
            "+34": "Spain", "+36": "Hungary", "+39": "Italy",
            "+40": "Romania", "+41": "Switzerland", "+43": "Austria",
            "+45": "Denmark", "+46": "Sweden", "+47": "Norway",
            "+48": "Poland", "+49": "Germany", "+51": "Peru",
            "+52": "Mexico", "+53": "Cuba", "+54": "Argentina",
            "+55": "Brazil", "+56": "Chile", "+57": "Colombia",
            "+58": "Venezuela", "+61": "Australia", "+64": "New Zealand",
            "+93": "Afghanistan", "+95": "Myanmar", "+98": "Iran",
            "+212": "Morocco", "+213": "Algeria", "+216": "Tunisia",
            "+218": "Libya", "+233": "Ghana", "+234": "Nigeria",
            "+254": "Kenya", "+255": "Tanzania", "+256": "Uganda",
            "+263": "Zimbabwe", "+351": "Portugal", "+352": "Luxembourg",
            "+353": "Ireland", "+354": "Iceland", "+355": "Albania",
            "+356": "Malta", "+357": "Cyprus", "+358": "Finland",
            "+359": "Bulgaria", "+380": "Ukraine", "+381": "Serbia",
            "+385": "Croatia", "+386": "Slovenia", "+420": "Czech Republic",
            "+421": "Slovakia",
        }

        if not country and country_code:
            cc_digits = re.sub(r"\D", "", country_code)
            sorted_codes = sorted(country_map.items(), key=lambda x: -len(re.sub(r"\D", "", x[0])))
            for code, name in sorted_codes:
                if cc_digits.startswith(re.sub(r"\D", "", code)):
                    country = name
                    break

        if not country:
            country = "Unknown"

        phone_str = re.sub(r"\D", "", str(phone).strip())

        return {
            "Telegram ID": str(tg_id),
            "Phone": phone_str,
            "Country": country,
            "Country Code": country_code or "N/A",
            "developer": DEVELOPER
        }

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
