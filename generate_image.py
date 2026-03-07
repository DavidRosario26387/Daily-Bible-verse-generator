from io import BytesIO
import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

FREEPIK_API_KEY = os.getenv("freepik_api_key")
BASE_URL = "https://api.freepik.com/v1/ai/mystic"


def generate(prompt: str) -> bytes:

    headers = {"x-freepik-api-key": FREEPIK_API_KEY,"Content-Type": "application/json",}

    payload = {"prompt": prompt,"resolution": "2k","aspect_ratio": "social_story_9_16","model": "realism"}

    r = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()

    task_id = r.json()["data"]["task_id"]

    status = "CREATED"
    image_url = None

    for _ in range(60):   # 60 checks × 5 seconds = max 5 minutes
        time.sleep(5)
        status_res = requests.get(f"{BASE_URL}/{task_id}",headers=headers,timeout=30)
        status_res.raise_for_status()
        data = status_res.json().get("data", {})
        status = data.get("status")
        if status == "COMPLETED":
            image_url = data["generated"][0]
            break
        if status == "FAILED":
            raise Exception("Image generation failed")
    if not image_url:
        raise Exception("Image generation timeout")

    img = requests.get(image_url, timeout=60)
    img.raise_for_status()

    return img.content
