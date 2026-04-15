import requests
import time

BOT_TOKEN = "8713603965:AAHL7rC9gRrEIGWh591HoYdz_9DD4Qym9Ok"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    return requests.get(url, params=params).json()

def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def send_video(chat_id, file_path):
    with open(file_path, "rb") as f:
        requests.post(f"{BASE_URL}/sendVideo", data={
            "chat_id": chat_id
        }, files={
            "video": f
        })

def download_video(url):
    headers = {
        "Referer": "https://www.xfree.com/",
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, stream=True)

    if r.status_code != 200:
        return None

    filename = "video.mp4"

    with open(filename, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    return filename

def main():
    offset = None

    while True:
        data = get_updates(offset)

        for update in data["result"]:
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                send_message(chat_id, "Send me a video link 😏")

            elif text.startswith("http"):
                send_message(chat_id, "Downloading... ⏳")

                file = download_video(text)

                if file:
                    send_message(chat_id, "Uploading... 🚀")
                    send_video(chat_id, file)
                else:
                    send_message(chat_id, "❌ Failed to download video")

        time.sleep(2)

if __name__ == "__main__":
    main()
