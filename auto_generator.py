import requests
import re
import time

def get_token(stream_id):
    url = f"http://tv.bdixbd.org/player.php?stream={stream_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # স্ক্রিপ্ট ট্যাগ বা প্লেয়ার সোর্স থেকে টোকেন খোঁজা
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

# আপনার দেওয়া ডিটেইলস থেকে নিখুঁত পাথ এবং আইডি ম্যাপিং
channel_list = [
    {"name": "T-SPORTS HD", "id": "1", "path": "/T-SPORTS-HD/index.m3u8"},
    {"name": "SONY SPORTS 1 HD", "id": "74", "path": "/SONY.SPORTS.1HD/index.m3u8"},
    {"name": "SONY SPORTS 2 HD", "id": "29", "path": "/SONY.SPORTS2.HD/index.m3u8"},
    {"name": "SONY SPORTS 3 HD", "id": "30", "path": "/SONY.SPORTS.3/index.m3u8"},
    {"name": "SONY SPORTS 5 HD", "id": "101", "path": "/SONY-SPORTS.5HD/index.m3u8"},
    {"name": "STAR SPORTS 1 HD", "id": "99", "path": "/STAR.SPORTS1.HD/index.m3u8"},
    {"name": "STAR SPORTS 2 HD", "id": "43", "path": "/STAR.SPORTS2.HD/index.m3u8"},
    {"name": "STAR SPORTS 3", "id": "57", "path": "/STAR-SPORTS.3/index.m3u8"},
    {"name": "STAR SPORTS SELECT 1", "id": "39", "path": "/STAR.SPORTS-SEL1.HD/index.m3u8"},
    {"name": "STAR SPORTS SELECT 2", "id": "33", "path": "/STAR.SPORTS.SEL.2.HD/index.m3u8"},
    {"name": "A SPORTS HD", "id": "88", "path": "/A.SPORTS.HD/index.m3u8"},
    {"name": "PTV SPORTS HD", "id": "92", "path": "/PTV-SPORTS-HD/index.m3u8"},
    {"name": "GTV (GAZI TV)", "id": "56", "path": "/stream-56/index.m3u8"},
    {"name": "SOMOY TV", "id": "79", "path": "/stream-79/index.m3u8"},
    {"name": "NTV", "id": "54", "path": "/stream-54/index.m3u8"}
]

m3u_content = "#EXTM3U\n"

print("🔄 Generating Playlist with the latest Star Sports folder structure...")

for ch in channel_list:
    token = get_token(ch["id"])
    if token:
        # Master URL format
        final_url = f"http://103.144.89.251:8082{ch['path']}?token={token}&remote=no_check_ip"
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n{final_url}\n'
        print(f"✅ {ch['name']} - Token Synced")
    else:
        print(f"❌ {ch['name']} - Token Failed")
    
    time.sleep(0.5) 

with open("playlist.m3u8", "w") as f:
    f.write(m3u_content)

print("\n🚀 Done! All Star Sports channels are now mapped correctly.")
