import requests
import re

def get_token():
    # BDIX সার্ভারের প্লেয়ার লিঙ্ক যেখান থেকে টোকেন স্ক্র্যাপ করা হবে
    url = "http://tv.bdixbd.org/player.php?stream=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

token = get_token()

if token:
    # চ্যানেল লিস্ট এবং তাদের পাথ
    channels = [
        {"name": "T-SPORTS HD", "path": "/T-SPORTS-HD/index.m3u8", "logo": "https://raw.githubusercontent.com/nrjtvbd/my-iptv/main/logos/tsports.png"},
        {"name": "GTV (Gazi TV)", "path": "/stream-56/index.m3u8", "logo": ""},
        {"name": "SONY SPORTS 1 HD", "path": "/SONY-SPORTS-1-HD/index.m3u8", "logo": ""},
        {"name": "SONY SPORTS 2 HD", "path": "/SONY-SPORTS-2-HD/index.m3u8", "logo": ""},
        {"name": "SONY SPORTS 3 HD", "path": "/SONY-SPORTS-3-HD/index.m3u8", "logo": ""},
        {"name": "SONY SPORTS 5 HD", "path": "/SONY-TEN-5-HD/index.m3u8", "logo": ""},
        {"name": "STAR SPORTS 1 HD", "path": "/STAR-SPORTS-1-HD/index.m3u8", "logo": ""},
        {"name": "STAR SPORTS 2 HD", "path": "/STAR-SPORTS-2-HD/index.m3u8", "logo": ""},
        {"name": "STAR SPORTS SELECT 1", "path": "/STAR-SPORTS-SELECT-1-HD/index.m3u8", "logo": ""},
        {"name": "SOMOY TV", "path": "/stream-79/index.m3u8", "logo": ""},
        {"name": "EKATTOR TV", "path": "/stream-24/index.m3u8", "logo": ""},
        {"name": "NTV", "path": "/stream-54/index.m3u8", "logo": ""},
    ]

    m3u_content = "#EXTM3U\n"
    for ch in channels:
        m3u_content += f'#EXTINF:-1 tvg-logo="{ch["logo"]}", {ch["name"]}\n'
        m3u_content += f'http://103.144.89.251:8082{ch["path"]}?token={token}&remote=no_check_ip\n'

    with open("playlist.m3u8", "w") as f:
        f.write(m3u_content)
    print(f"Successfully updated {len(channels)} channels with new token!")
else:
    print("Failed to fetch fresh token.")
