import os
from dotenv import load_dotenv
import requests,json

load_dotenv()

groq_api_key=os.getenv("llm_api_key")

def call_llm(prompt, expect_json=False, retries=3):
    url = "https://api.groq.com/openai/v1/responses"
    headers= {"Content-Type": "application/json","Authorization": f"Bearer {groq_api_key}"}
    data = {"model": "llama-3.3-70b-versatile","temperature": 0.8,"input": prompt}
    for attempt in range(retries):
        res = requests.post(url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        response = res.json()
        text = None
        for item in response.get("output", []):
            if item.get("type") == "message":
                content = item.get("content", [])
                if content:
                    text = content[0].get("text")
                break
        if text is None:
            continue
        text = text.strip()
        if expect_json:
            try:
                json.loads(text)
                return text
            except json.JSONDecodeError:
                if attempt == retries - 1:
                    raise Exception("LLM returned invalid JSON")
                continue
        else:
            return text
    raise Exception("LLM response parsing failed")
