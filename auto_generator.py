import requests
import re

def get_token():
    # বিডিক্স সার্ভারের প্লেয়ার লিঙ্ক
    url = "http://tv.bdixbd.org/player.php?stream=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # HTML থেকে টোকেনটি খুঁজে বের করা
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

token = get_token()

if token:
    m3u8_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="tsports" tvg-logo="https://raw.githubusercontent.com/nrjtvbd/my-iptv/main/logo.png", T-SPORTS HD
http://103.144.89.251:8082/T-SPORTS-HD/index.m3u8?token={token}&remote=no_check_ip
#EXTINF:-1 tvg-id="gtv" tvg-logo="", GTV
http://103.144.89.251:8082/stream-56/index.m3u8?token={token}&remote=no_check_ip
"""
    with open("playlist.m3u8", "w") as f:
        f.write(m3u8_content)
    print("Token updated successfully!")
else:
    print("Failed to get token.")
