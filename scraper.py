import requests
from bs4 import BeautifulSoup
from datetime import date
import json

today = date.today()
url = f"https://www.esbnyc.com/about/tower-lights/calendar/{today.strftime('%Y%m')}"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

resp = requests.get(url, headers=headers)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
entry = soup.find("article", attrs={"data-date": today.isoformat()})

if entry:
    color = entry.find("div", class_="name").get_text(strip=True)
    desc = entry.find("div", class_="field_description")
    reason = desc.get_text(strip=True) if desc else ""
else:
    color = "Signature White"
    reason = "The Empire State Building's signature look"

result = {"date": today.isoformat(), "color": color, "reason": reason}

with open("esb_tonight.json", "w") as f:
    json.dump(result, f, indent=2)

print("Wrote:", json.dumps(result))
