import requests
import re
import time

def get_token(stream_id):
    # প্রতিটি চ্যানেলের নির্দিষ্ট প্লেয়ার পেজ থেকে টোকেন নেওয়া
    url = f"http://tv.bdixbd.org/player.php?stream={stream_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # HTML সোর্স থেকে টোকেনটি খুঁজে বের করা
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

# সংগৃহীত সঠিক পাথ এবং আইডি লিস্ট
channel_list = [
    {"name": "T-SPORTS HD", "id": "1", "path": "/T-SPORTS-HD/index.m3u8"},
    {"name": "SONY SPORTS 1 HD", "id": "74", "path": "/SONY-SPORTS-1-HD/index.m3u8"},
    {"name": "SONY SPORTS 2 HD", "id": "29", "path": "/SONY.SPORTS2.HD/index.m3u8"},
    {"name": "SONY SPORTS 3 HD", "id": "30", "path": "/SONY-SPORTS-3/tracks-v1a1/mono.m3u8"},
    {"name": "SONY SPORTS 5 HD", "id": "101", "path": "/SONY-TEN-5-HD/tracks-v1a1/mono.m3u8"},
    {"name": "A SPORTS HD", "id": "88", "path": "/stream-88/index.m3u8"},
    {"name": "GTV (GAZI TV)", "id": "56", "path": "/stream-56/index.m3u8"},
    {"name": "SOMOY TV", "id": "79", "path": "/stream-79/index.m3u8"},
    {"name": "NTV", "id": "54", "path": "/stream-54/index.m3u8"},
    {"name": "CHANNEL 24", "id": "82", "path": "/stream-82/index.m3u8"},
]

m3u_content = "#EXTM3U\n"

print("Starting token collection for all channels...")

for ch in channel_list:
    token = get_token(ch["id"])
    if token:
        # লিঙ্ক তৈরি করা (টোকেনসহ)
        final_url = f"http://103.144.89.251:8082{ch['path']}?token={token}&remote=no_check_ip"
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n{final_url}\n'
        print(f"✅ Success: {ch['name']}")
    else:
        print(f"❌ Failed: {ch['name']}")
    
    # সার্ভারে চাপ কমাতে সামান্য বিরতি
    time.sleep(1)

# প্লেলিস্ট ফাইল তৈরি
with open("playlist.m3u8", "w") as f:
    f.write(m3u_content)

print("\n--- Final Playlist Generated Successfully ---")
