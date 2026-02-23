import requests
import re

def get_link():
    # প্রথম সোর্স: BDIXBD
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get("http://tv.bdixbd.org/", headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', r.text)
        if match:
            token = match.group(1)
            return f"http://103.144.89.251:8082/T-SPORTS-HD/mono.m3u8?token={token}&remote=no_check_ip"
    except:
        pass

    # দ্বিতীয় সোর্স: RoarZone (যদি প্রথমটি কাজ না করে)
    try:
        r = requests.get("https://roarzone.info/tv/tsports", timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', r.text)
        if match:
            token = match.group(1)
            return f"https://edge2.roarzone.info:444/roarzone/edge2/tsports/index.m3u8?token={token}"
    except:
        pass
        
    return None

def main():
    final_link = get_link()
    if final_link:
        content = f"#EXTM3U\n#EXTINF:-1,T-Sports HD\n{final_link}"
        with open("playlist.m3u8", "w") as f:
            f.write(content)
        print("✅ Success: New token found and saved in playlist.m3u8")
    else:
        print("❌ Error: Could not fetch token from any source.")

if __name__ == "__main__":
    main()
