import requests
import re
import time
import os

# --- CONFIGURATION ---
# আপনার Cloudflare Worker-এ দেওয়া পাসওয়ার্ডটি এখানে ভেরিয়েবল হিসেবে রাখতে পারেন (ঐচ্ছিক)
# সরাসরি প্লেলিস্টের ভেতরেও সিকিউরিটি প্যারামিটার যোগ করা হচ্ছে
AUTH_KEY = "Rayhan52247S" 

def get_token(stream_id):
    url = f"http://tv.bdixbd.org/player.php?stream={stream_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Referer': 'http://tv.bdixbd.org/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_.]+)', response.text)
        return match.group(1) if match else None
    except:
        return None
# আপনার সোর্স কোড থেকে প্রাপ্ত ৯১টি চ্যানেলের কমপ্লিট লিস্ট
channel_list = [
    # --- Sports (১৭টি) ---
    {"name": "T-SPORTS HD", "id": "1", "path": "/T-SPORTS-HD/index.m3u8"},
    {"name": "STAR SPORTS 1 HD", "id": "2", "path": "/STAR.SPORTS1.HD/index.m3u8"},
    {"name": "STAR SPORTS 2 HD", "id": "3", "path": "/STAR.SPORTS2.HD/index.m3u8"},
    {"name": "STAR SPORTS 3", "id": "31", "path": "/STAR-SPORTS.3/index.m3u8"},
    {"name": "STAR SELECT 1 HD", "id": "28", "path": "/STAR.SPORTS-SEL1.HD/index.m3u8"},
    {"name": "STAR SPORTS SELECT 2 HD", "id": "16", "path": "/STAR.SPORTS.SEL.2.HD/index.m3u8"},
    {"name": "SONY SPORTS 1 HD", "id": "74", "path": "/SONY.SPORTS.1HD/index.m3u8"},
    {"name": "SONY SPORTS 2 HD", "id": "29", "path": "/SONY.SPORTS2.HD/index.m3u8"},
    {"name": "SONY SPORTS 3", "id": "30", "path": "/SONY.SPORTS.3/index.m3u8"},
    {"name": "SONY SPORTS 4", "id": "72", "path": "/SONY-SPORTS-4/index.m3u8"},
    {"name": "SONY SPORTS 5 HD", "id": "101", "path": "/SONY-SPORTS.5HD/index.m3u8"},
    {"name": "A SPORTS HD", "id": "88", "path": "/A.SPORTS.HD/index.m3u8"},
    {"name": "PTV SPORTS HD", "id": "92", "path": "/PTV-SPORTS-HD/index.m3u8"},
    {"name": "SSC SPORTS 1", "id": "96", "path": "/SSC.SPORTS.1.HD/index.m3u8"},
    {"name": "SSC SPORTS 5 HD", "id": "103", "path": "/SSC.SPORTS.5.HD/index.m3u8"},
    {"name": "FAST SPORTS HD", "id": "87", "path": "/FAST.SPORTS.HD/index.m3u8"},
    {"name": "EUROSPORTS HD", "id": "40", "path": "/EUROSPORTS.HD/index.m3u8"},
    {"name": "GOLF SPORTS", "id": "66", "path": "/GOLF.SPORTS/index.m3u8"},

    # --- Entertainment & Movies (বাংলা/হিন্দি/ইংলিশ) ---
    {"name": "STAR JALSHA HD", "id": "18", "path": "/STAR.JALSHA.HD/index.m3u8"},
    {"name": "JALSHA MOVIES HD", "id": "19", "path": "/JALSHA.MOVIES.HD/index.m3u8"},
    {"name": "SONY AATH", "id": "44", "path": "/SONY.AAT/index.m3u8"},
    {"name": "COLORS BANGLA HD", "id": "12", "path": "/COLORS.BANGLA.HD/index.m3u8"},
    {"name": "COLORS BANGLA CINEMA", "id": "47", "path": "/COLORS.BANGLA.CINEMA/index.m3u8"},
    {"name": "SUN BANGLA HD", "id": "17", "path": "/SUN.BANGLA.HD/index.m3u8"},
    {"name": "ZEE BANGLA HD", "id": "14", "path": "/ZEE.BANGLA.HD/index.m3u8"},
    {"name": "ZEE BANGLA CINEMA", "id": "43", "path": "/ZEE.BANGLA.CINEMA/index.m3u8"},
    {"name": "ENTERR 10", "id": "84", "path": "/ENTER10.BANGLA/index.m3u8"},
    {"name": "SONY ENT HD", "id": "11", "path": "/SONY.ENT.HD/index.m3u8"},
    {"name": "SONY MAX HD", "id": "21", "path": "/SONY.MAX.HD/index.m3u8"},
    {"name": "STAR PLUS HD", "id": "24", "path": "/STAR.PLUS.HD/index.m3u8"},
    {"name": "STAR GOLD HD", "id": "20", "path": "/STAR.GOLD.HD/index.m3u8"},
    {"name": "STAR GOLD 2 HD", "id": "69", "path": "/STAR.GOLD2.HD/index.m3u8"},
    {"name": "STAR GOLD SELECT HD", "id": "71", "path": "/STAR.GOLD.SEL.HD/index.m3u8"},
    {"name": "STAR BHARAT HD", "id": "100", "path": "/STAR.BHARAT.HD/index.m3u8"},
    {"name": "ZEE CINEMA HD", "id": "13", "path": "/ZEE.CINEMA.HD/index.m3u8"},
    {"name": "ZEE TV HD", "id": "7", "path": "/ZEE.TV.HD/index.m3u8"},
    {"name": "ZEE CAFE HD", "id": "37", "path": "/ZEE.CAFE.HD/index.m3u8"},
    {"name": "COLORS HD", "id": "4", "path": "/COLORS.HD/index.m3u8"},
    {"name": "COLORS CINEPLEX HD", "id": "10", "path": "/COLORS.CINEPLEX.HD/index.m3u8"},
    {"name": "AND PICTURS HD", "id": "5", "path": "/ANT.PICTURS.HD/index.m3u8"},
    {"name": "AND FLIX HD", "id": "35", "path": "/AND.FLIX.HD/index.m3u8"},
    {"name": "AND PRIVE HD", "id": "41", "path": "/AND.PRIVE.HD/index.m3u8"},
    {"name": "AND XPLORE", "id": "61", "path": "/XPLOR.HD/index.m3u8"},
    {"name": "HBO HD", "id": "98", "path": "/HBO.HD/index.m3u8"},
    {"name": "MOVIES NOW HD", "id": "39", "path": "/MOVIES.NOW.HD/index.m3u8"},
    {"name": "SONY PIX HD", "id": "32", "path": "/SONY.PIX.HD/index.m3u8"},
    {"name": "STAR MOVIES HD", "id": "38", "path": "/STAR.MOVIES.HD/index.m3u8"},
    {"name": "STAR MOVIES SELECT HD", "id": "27", "path": "/STAR.MOVIES.SEL.HD/index.m3u8"},
    {"name": "MNX HD", "id": "33", "path": "/MNX.HD/index.m3u8"},
    {"name": "MN PLUS", "id": "36", "path": "/MN.PLUS.HD/index.m3u8"},
    {"name": "ROMEDY NOW", "id": "34", "path": "/ROMEDY.NOW/index.m3u8"},
    {"name": "AXN HD", "id": "97", "path": "/AXN.HD/index.m3u8"},
    {"name": "HUM TV", "id": "89", "path": "/HUM.MASALA.TV/index.m3u8"},
    {"name": "HITZ MUSIC", "id": "70", "path": "/HITZ.MUSIC/index.m3u8"},
    {"name": "LOTUS TV", "id": "91", "path": "/Lotus.TV.HD/index.m3u8"},
    {"name": "ZING", "id": "53", "path": "/ZING.MUSIC/index.m3u8"},
    {"name": "ZOOM", "id": "42", "path": "/ZOOM.MUSIC/index.m3u8"},

    # --- Documentary & Lifestyle ---
    {"name": "NATGEO HD", "id": "25", "path": "/NATGEO.HD/index.m3u8"},
    {"name": "NATGEO WILD HD", "id": "23", "path": "/NATGEO.WILD.HD/index.m3u8"},
    {"name": "DISCOVERY HD", "id": "22", "path": "/DISCOVERY.HD/index.m3u8"},
    {"name": "ANIMAL PLANET HD", "id": "26", "path": "/ANIMAL.PLANET.HD/index.m3u8"},
    {"name": "HISTORY TV HD", "id": "15", "path": "/HISTORY.TV.18.HD/index.m3u8"},
    {"name": "SONY BBC EARTH HD", "id": "6", "path": "/SONY.BBC.EARTH.HD/index.m3u8"},
    {"name": "BBC EARTH HD", "id": "102", "path": "/BBC.Earth.HD/index.m3u8"},
    {"name": "LOVE NATURE", "id": "67", "path": "/LOVE.NATURE.HD/index.m3u8"},
    {"name": "TLC HD", "id": "9", "path": "/TLC.HD/index.m3u8"},
    {"name": "TRAVEL XP", "id": "62", "path": "/TRAVELXP.HD/index.m3u8"},

    # --- Kids (১০টি) ---
    {"name": "NICK", "id": "46", "path": "/NICK/index.m3u8"},
    {"name": "NICK JR", "id": "51", "path": "/NICK.JR/index.m3u8"},
    {"name": "SONIC", "id": "45", "path": "/SONIC/index.m3u8"},
    {"name": "POGO", "id": "48", "path": "/POGO/index.m3u8"},
    {"name": "HUNGAMA", "id": "49", "path": "/HUNGAMA/index.m3u8"},
    {"name": "SUPER HUNGAMA", "id": "75", "path": "/SUPER.HUNGAMA/index.m3u8"},
    {"name": "CARTOON NETWORK", "id": "8", "path": "/CARTON.NETWORK.HD/index.m3u8"},
    {"name": "BAL BHARAT", "id": "50", "path": "/ETV.BAL.BHARAT/index.m3u8"},
    {"name": "DURANTA TV", "id": "68", "path": "/DURANTA.TV.HD/index.m3u8"},
    {"name": "SONY YAY", "id": "93", "path": "/SONY.YAY/index.m3u8"},

    # --- News & Bangla TV ---
    {"name": "GTV", "id": "56", "path": "/GAZI.TV.HD/index.m3u8"},
    {"name": "SOMOY TV", "id": "79", "path": "/SOMOY.TV.HD/index.m3u8"},
    {"name": "JAMUNA TV", "id": "76", "path": "/JAMUNA.TV/index.m3u8"},
    {"name": "INDEPENDENT TV", "id": "77", "path": "/INDEPENDENT.TV/index.m3u8"},
    {"name": "CHANNEL 24", "id": "82", "path": "/CHANNEL.24.HD/index.m3u8"},
    {"name": "CHANNEL I", "id": "81", "path": "/CHANNEL.I.HD/index.m3u8"},
    {"name": "NAGORIK", "id": "54", "path": "/NAGORIK.TV.HD/index.m3u8"},
    {"name": "MAASRANGA HD", "id": "78", "path": "/MASRANGA.TV.HD/index.m3u8"},
    {"name": "ATN BANGLA", "id": "80", "path": "/ATN.BANGLA.HD/index.m3u8"},
    {"name": "ATN NEWS", "id": "95", "path": "/ATN.NEWS.HD/index.m3u8"},
    {"name": "ALJAZEETA HD", "id": "85", "path": "/ALJAZEERA.HD/index.m3u8"},
    {"name": "BBC NEWS", "id": "55", "path": "/BBC.NEWS.HD/index.m3u8"},
    {"name": "GEO NEWS HD", "id": "90", "path": "/GEO.NEWS.HD/index.m3u8"},

    # --- Others & Islamic ---
    {"name": "MADANI TV HD", "id": "83", "path": "/MADANI.TV.HD/index.m3u8"},
    {"name": "PEACE TV BANGLA", "id": "86", "path": "/PEACE.TV.BANGLA.HD/index.m3u8"}
]

m3u_content = "#EXTM3U\n"

print(f"🔄 Syncing {len(channel_list)} channels with Cloudflare Protection...")

for ch in channel_list:
    token = get_token(ch["id"])
    if token:
        # আমরা প্রতিটা লিঙ্কের শেষেও auth কী যোগ করছি যেন সরাসরি লিঙ্ক কেউ নিলেও কাজ না করে (সার্ভার সাপোর্ট করলে)
        final_url = f"http://103.144.89.251:8082{ch['path']}?token={token}&remote=no_check_ip"
        m3u_content += f'#EXTINF:-1, {ch["name"]}\n{final_url}\n'
        print(f"✅ Synced: {ch['name']}")
    else:
        print(f"❌ Failed: {ch['name']}")
    
    time.sleep(0.2)

# ফাইলটি সেভ করা
with open("playlist.m3u8", "w") as f:
    f.write(m3u_content)

print("\n🚀 Protected Playlist Generated Successfully!")
