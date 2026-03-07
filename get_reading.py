import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

# ---------- get tomorrow readings ----------
def get_tmrw_reading():
    date = (datetime.now() + timedelta(days=1)).strftime("%m%d%y")
    url = f"https://bible.usccb.org/bible/readings/{date}.cfm"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    # title
    title = soup.find("div", class_="b-lectionary").find("h2").get_text(strip=True)
    data["title"] = title
    # each reading block
    for block in soup.find_all("div", class_="b-verse"):

        header = block.find("h3", class_="name")
        ref = block.find("div", class_="address")
        body = block.find("div", class_="content-body")
        if not header:
            continue
        key = header.get_text(strip=True).lower().replace(" ", "_")
        reference = ""
        if ref and ref.find("a"):
            reference = ref.find("a").get_text(strip=True)
        text = ""
        if body:
            text = " ".join(body.stripped_strings)
        data[key] = {"reference": reference,"text": text}

    return json.dumps(data, indent=2, ensure_ascii=False)
