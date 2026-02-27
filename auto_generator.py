import requests
import re

def get_token():
    # বিডিক্স সার্ভারের প্লেয়ার লিঙ্ক যেখান থেকে টোকেন স্ক্র্যাপ করা হবে
    url = "http://tv.bdixbd.org/player.php?stream=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # HTML থেকে টোকেনটি খুঁজে বের করা
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None

token = get_token()

if token:
    # আপনার দেওয়া HTML সোর্স থেকে সংগৃহীত চ্যানেলের লিস্ট
    channels = [
        {"name": "T-SPORTS HD", "path": "/T-SPORTS-HD/index.m3u8"},
        {"name": "GTV (GAZI TV)", "path": "/stream-56/index.m3u8"},
        {"name": "A SPORTS HD", "path": "/stream-88/index.m3u8"},
        {"name": "SONY SPORTS 1 HD", "path": "/SONY-SPORTS-1-HD/index.m3u8"},
        {"name": "SONY SPORTS 2 HD", "path": "/SONY-SPORTS-2-HD/index.m3u8"},
        {"name": "SONY SPORTS 3", "path": "/SONY-SPORTS-3/index.m3u8"},
        {"name": "SONY SPORTS 5 HD", "path": "/SONY-TEN-5-HD/index.m3u8"},
        {"name": "STAR SPORTS 1 HD", "path": "/STAR-SPORTS-1-HD/index.m3u8"},
        {"name": "STAR SPORTS 2 HD", "path": "/STAR-SPORTS-2-HD/index.m3u8"},
        {"name": "PTV SPORTS HD", "path": "/stream-92/index.m3u8"},
        {"name": "SSC SPORTS 1 HD", "path": "/stream-96/index.m3u8"},
        {"name": "SSC SPORTS 5 HD", "path": "/stream-103/index.m3u8"},
        {"name": "COLORS HD", "path": "/stream-4/index.m3u8"},
        {"name": "SONY ENT HD", "path": "/stream-11/index.m3u8"},
        {"name": "STAR BHARAT HD", "path": "/stream-100/index.m3u8"},
        {"name": "JALSHA MOVIES HD", "path": "/stream-19/index.m3u8"},
        {"name": "COLORS BANGLA HD", "path": "/stream-12/index.m3u8"},
        {"name": "SOMOY TV", "path": "/stream-79/index.m3u8"},
        {"name": "INDEPENDENT TV", "path": "/stream-77/index.m3u8"},
        {"name": "JAMUNA TV", "path": "/stream-76/index.m3u8"},
        {"name": "CHANNEL 24", "path": "/stream-82/index.m3u8"},
        {"name": "ATN BANGLA", "path": "/stream-80/index.m3u8"},
        {"name": "NTV", "path": "/stream-54/index.m3u8"},
        {"name": "DURANTA TV", "path": "/stream-68/index.m3u8"},
        {"name": "NICK", "path": "/stream-46/index.m3u8"},
        {"name": "POGO", "path": "/stream-48/index.m3u8"},
        {"name": "CARTOON NETWORK", "path": "/stream-8/index.m3u8"},
        {"name": "PEACE TV BANGLA", "path": "/stream-86/index.m3u8"},
    ]

    m3u_content = "#EXTM3U\n"
    for ch in channels:
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n'
        # প্রতিটি চ্যানেলের জন্য একই টোকেন ব্যবহার করে লিঙ্ক তৈরি
        m3u_content += f'http://103.144.89.251:8082{ch["path"]}?token={token}&remote=no_check_ip\n'

    with open("playlist.m3u8", "w") as f:
        f.write(m3u_content)
    print(f"Successfully updated {len(channels)} channels with new token!")
else:
    print("Failed to fetch fresh token.")
