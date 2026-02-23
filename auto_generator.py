import requests
import re

def get_link():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get("https://roarzone.info/tv/tsports", headers=headers, timeout=15)
        token = re.search(r'token=([a-zA-Z0-9\-_.]+)', r.text).group(1)
        return f"https://edge2.roarzone.info:444/roarzone/edge2/tsports/index.m3u8?token={token}"
    except:
        return None

final_link = get_link()
if final_link:
    with open("playlist.m3u8", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,T-Sports HD\n{final_link}")
