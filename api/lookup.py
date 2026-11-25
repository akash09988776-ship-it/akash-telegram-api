import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ⚠️ YAHAN APNA REAL API KA URL DAALEIN (Isko response mein kabhi mat bhejna)
REAL_API_URL = "https://real-api-url-here.com/v1/tg-lookup" 
# Example: REAL_API_URL = "https://api.example.com/v1/lookup"

# Aapka custom API key (jo aap apne custom URL mein use kar rahe hain)
CUSTOM_API_KEY = "z9x7q2m" 

# Developer branding
DEVELOPER_NAME = "ᴀᴋᴀꜱʜ ᴏꜱɪɴᴛ"

@app.route('/v1/tg-lookup-z9x7q2m', methods=['GET'])
def tg_lookup():
    # 1. Custom API Key check karein (Security ke liye)
    key = request.args.get('key')
    if key != CUSTOM_API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    # 2. Query (Telegram ID) lein
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # 3. Real API ko call karein
    try:
        # Real API ko request bhejein (Yahan aapko real API ka key/params dalna hoga)
        # Agar real API ko koi key chahiye, toh headers ya params mein daalein
        real_response = requests.get(
            REAL_API_URL, 
            params={"query": query}, 
            timeout=10 # 10 second timeout
        )
        real_data = real_response.json()
        
        # 4. Check karein ki real API ne data diya ya nahi
        if not real_data.get("status") or "tg_id" not in real_data:
            # Agar real API mein user nahi mila, toh custom "Not Found" response
            return jsonify({
                "status": False,
                "message": "No data found for this Telegram ID."
            }), 404

        # 5. Data ko aapke format mein convert karein
        tg_id = real_data.get("tg_id", "N/A")
        phone_list = real_data.get("phone", [])
        
        # Phone list se pehla number, country, country code nikaalein
        if phone_list and len(phone_list) > 0:
            phone_info = phone_list[0]
            phone_number = phone_info.get("number", "N/A")
            country_code = phone_info.get("country_code", "N/A")
            country_name = phone_info.get("country", "N/A")
        else:
            phone_number = "N/A"
            country_code = "N/A"
            country_name = "N/A"

        # 6. Aapka Custom Response Format
        custom_response = (
            f"🆔 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 • {tg_id}\n"
            f"📞 𝗣𝗵𝗼𝗻𝗲 • {phone_number}\n"
            f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 • {country_name}\n"
            f"📡 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲 • {country_code}\n\n"
            f"├ 🛠️ ᴅᴇᴠᴇʟᴏᴘᴇʀ: {DEVELOPER_NAME} • 🛰️"
        )

        return jsonify({
            "status": True,
            "response": custom_response
        })

    except requests.exceptions.Timeout:
        return jsonify({"status": False, "message": "Real API request timed out."}), 504
    except requests.exceptions.RequestException as e:
        # Real API URL ya error kabhi bhi response mein mat bhejein
        return jsonify({"status": False, "message": "Internal Server Error"}), 500
    except Exception as e:
        return jsonify({"status": False, "message": "An unexpected error occurred."}), 500

# Vercel ke liye handler (agar zaroorat ho)
def handler(request, context):
    return app(request.environ, context)
