import requests
import re

def get_token(stream_id):
    # প্রতিটি চ্যানেলের নির্দিষ্ট প্লেয়ার পেজ থেকে টোকেন নেওয়া
    url = f"http://tv.bdixbd.org/player.php?stream={stream_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # HTML সোর্স থেকে টোকেনটি খুঁজে বের করা
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

# চ্যানেলের তালিকা (নাম, স্ট্রিম আইডি, এবং সঠিক ভিডিও পাথ)
channel_list = [
    {"name": "T-SPORTS HD", "id": "1", "path": "/T-SPORTS-HD/index.m3u8"},
    {"name": "SONY SPORTS 1 HD", "id": "74", "path": "/SONY-SPORTS-1-HD/index.m3u8"},
    {"name": "GTV (GAZI TV)", "id": "56", "path": "/stream-56/index.m3u8"},
    {"name": "A SPORTS HD", "id": "88", "path": "/stream-88/index.m3u8"},
    {"name": "SOMOY TV", "id": "79", "path": "/stream-79/index.m3u8"},
    {"name": "NTV", "id": "54", "path": "/stream-54/index.m3u8"},
    {"name": "STAR SPORTS 1 HD", "id": "104", "path": "/STAR-SPORTS-1-HD/index.m3u8"}
]

m3u_content = "#EXTM3U\n"

print("Starting token collection for each channel...")

for ch in channel_list:
    token = get_token(ch["id"])
    if token:
        # লিঙ্ক তৈরি করা (টোকেনসহ)
        final_url = f"http://103.144.89.251:8082{ch['path']}?token={token}&remote=no_check_ip"
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n{final_url}\n'
        print(f"Successfully fetched token for {ch['name']}")
    else:
        print(f"Failed to fetch token for {ch['name']}")

# ফাইল সেভ করা
with open("playlist.m3u8", "w") as f:
    f.write(m3u_content)

print("Playlist updated with individual tokens!")
