import requests
import re
import os

def get_live_token():
    # এই URL টি মূলত টোকেন জেনারেটরের মূল সোর্স (উদাহরণস্বরূপ)
    url = "https://roarzone.info/tv/tsports" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://roarzone.info/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # এখানে আমরা টেক্সট থেকে টোকেনটি খুঁজে বের করার চেষ্টা করছি
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        if match:
            return match.group(1)
    except:
        pass
    return None

def main():
    token = get_live_token()
    if token:
        stream_url = f"https://edge2.roarzone.info:444/roarzone/edge2/tsports/index.m3u8?token={token}"
        content = f"#EXTM3U\n#EXTINF:-1,T-Sports HD\n{stream_url}"
        
        with open("playlist.m3u8", "w") as f:
            f.write(content)
        print("✅ New Token Found and Saved!")
    else:
        print("❌ Failed to fetch token.")

if __name__ == "__main__":
    main()
