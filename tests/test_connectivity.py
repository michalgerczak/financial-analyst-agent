import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_openai():
    print("\n--- CHECKING OPENAI ---")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("FAILED: Missing OPENAI_API_KEY in .env")
        return

    try:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.openai.com/v1/models", headers=headers)

        if response.status_code == 200:
            print("SUCCESS: Connection established.")
            models = [m['id'] for m in response.json()['data']]
            if "gpt-4o" in models:
                print("VERIFIED: Model 'gpt-4o' is available.")
            else:
                print("WARNING: 'gpt-4o' not listed (check billing).")
        else:
            print(f"FAILED: Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"FAILED: Connection Error: {e}")

def check_anthropic():
    print("\n--- CHECKING ANTHROPIC (Claude 4.5) ---")
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("FAILED: Missing ANTHROPIC_API_KEY in .env")
        return

    try:
        target_model = "claude-sonnet-4-5-20250929"

        headers = {
            "x-api-key": key, 
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": target_model,
            "max_tokens": 5,
            "messages": [{"role": "user", "content": "Hi"}]
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)

        if response.status_code == 200:
            print(f"SUCCESS: Connection established.")
            print(f"VERIFIED: '{target_model}' is active.")
        else:
            print(f"FAILED: Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"FAILED: Connection Error: {e}")

def check_llamacloud():
    print("\n--- CHECKING LLAMACLOUD ---")
    key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not key:
        print("FAILED: Missing LLAMA_CLOUD_API_KEY")
        return

    try:
        url = "https://api.cloud.llamaindex.ai/api/v1/parsing/upload"
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.post(url, headers=headers)

        if response.status_code in [400, 422]:
            print("SUCCESS: Connection established (Key accepted, waiting for file).")
        elif response.status_code == 401:
            print("FAILED: Error 401 Unauthorized. Key is invalid.")
        else:
            print(f"WARNING: Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"FAILED: Connection Error: {e}")

if __name__ == "__main__":
    check_openai()
    check_anthropic()
    check_llamacloud()