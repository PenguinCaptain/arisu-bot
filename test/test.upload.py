token = "fe1673c3349bbaef66cc63239800d5ae"
url = "https://api.imgbb.com/1/upload"

import requests
import base64

content = open("./src/res.png", "rb").read()

request = requests.post(url, {
    "expiration": 1200,
    "key": token,
    "image": base64.b64encode(content)
})

# request.json()["data"]["display_url"]