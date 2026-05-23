import requests

TELEGRAM_BOT_TOKEN = "8245149614:AAGxMSFmFYLypZWEySO-4TqJaU0nfLNedj8"
TELEGRAM_CHAT_ID = "8236339892"

message = "✅ Test from NIDS - Telegram is working!"

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

response = requests.post(url, json={
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message
})

print("Status Code:", response.status_code)
print("Response:", response.json())