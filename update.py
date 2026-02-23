import requests
import re
import os

# --- কনফিগারেশন ---
FILE_NAME = "playlist.m3u8"

def fetch_bdix_token():
    """সরাসরি bdixbd সাইট থেকে টোকেন নেওয়ার চেষ্টা"""
    url = "http://tv.bdixbd.org/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', r.text)
        if match:
            token = match.group(1)
            return f"http://103.144.89.251:8082/T-SPORTS-HD/mono.m3u8?token={token}&remote=no_check_ip"
    except:
        return None

def fetch_roarzone_token():
    """সরাসরি RoarZone সোর্স থেকে টোকেন বের করা (ওই ডেভেলপারের JSON ছাড়া)"""
    url = "https://roarzone.info/tv/tsports" # উদাহরণ সোর্স
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', r.text)
        if match:
            token = match.group(1)
            return f"https://edge2.roarzone.info:444/roarzone/edge2/tsports/index.m3u8?token={token}"
    except:
        return None

def main():
    # প্রথমে BDIXBD ট্রাই করবে, না হলে RoarZone
    final_url = fetch_bdix_token() or fetch_roarzone_token()
    
    if final_url:
        content = f"#EXTM3U\n#EXTINF:-1,T-Sports HD\n{final_url}"
        with open(FILE_NAME, "w") as f:
            f.write(content)
        print("✅ Success: Playlist updated from direct source!")
    else:
        print("❌ Error: All sources failed.")

if __name__ == "__main__":
    main()
