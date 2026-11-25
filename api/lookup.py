import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Aapka real API URL (response mein kabhi nahi jayega)
REAL_API_URL = "https://telegram2num.noobster11001.workers.dev/fast"
REAL_API_KEY = "noobster"

# Aapka custom key (URL same rakhne ke liye)
CUSTOM_API_KEY = "DEMO" 

DEVELOPER_NAME = "ᴀᴋᴀꜱʜ ᴏꜱɪɴᴛ"

@app.route('/v1/tg-lookup-z9x7q2m', methods=['GET'])
def tg_lookup():
    # 1. Custom key check
    key = request.args.get('key')
    if key != CUSTOM_API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    # 2. Query (Telegram ID)
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    try:
        # 3. Real API call (aapke real API ke hisaab se params)
        real_response = requests.get(
            REAL_API_URL,
            params={"key": REAL_API_KEY, "q": query},
            timeout=10
        )
        real_data = real_response.json()
        
        # 4. Data check karein (real API ka response structure)
        # Real API ka status check (agar status false ya tg_id nahi hai toh not found)
        if not real_data.get("status") or "tg_id" not in real_data:
            return jsonify({
                "status": False,
                "message": "No data found for this Telegram ID."
            }), 404

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

        # 6. Aapka custom format (real API ka koi extra data nahi)
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
    except requests.exceptions.RequestException:
        return jsonify({"status": False, "message": "Internal Server Error"}), 500
    except Exception:
        return jsonify({"status": False, "message": "An unexpected error occurred."}), 500
