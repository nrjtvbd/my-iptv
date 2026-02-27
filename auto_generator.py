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
        response = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

token = get_token()

if token:
    # সঠিক পাথ ম্যাপিং (আপনার দেওয়া ডাটা অনুযায়ী আপডেট করা)
    channels = [
        {"name": "T-SPORTS HD", "url": f"http://103.144.89.251:8082/T-SPORTS-HD/index.m3u8?token={token}&remote=no_check_ip"},
        {"name": "SONY SPORTS 1 HD", "url": f"http://103.144.89.251:8082/SONY-SPORTS-1-HD/tracks-v1a1/mono.m3u8?token={token}"},
        {"name": "GTV (GAZI TV)", "url": f"http://103.144.89.251:8082/stream-56/index.m3u8?token={token}&remote=no_check_ip"},
        {"name": "A SPORTS HD", "url": f"http://103.144.89.251:8082/stream-88/index.m3u8?token={token}&remote=no_check_ip"},
        {"name": "SOMOY TV", "url": f"http://103.144.89.251:8082/stream-79/index.m3u8?token={token}&remote=no_check_ip"},
        {"name": "NTV", "url": f"http://103.144.89.251:8082/stream-54/index.m3u8?token={token}&remote=no_check_ip"},
    ]

    m3u_content = "#EXTM3U\n"
    for ch in channels:
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n'
        m3u_content += f'{ch["url"]}\n'

    with open("playlist.m3u8", "w") as f:
        f.write(m3u_content)
    print("Playlist updated with new Sony Sports path!")
else:
    print("Failed to get token.")
