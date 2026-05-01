import json
from modules.api_detector import detect_apis
import requests
import google.generativeai as genai

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def check_api_status(url):
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)

        status_code = response.status_code

        if status_code == 200:
            return "OK (200)"
        elif status_code == 401:
            return "Unauthorized (401)"
        elif status_code == 403:
            return "Denied / Forbidden (403)"
        elif status_code == 404:
            return "Not Found (404)"
        else:
            return f"Other status ({status_code})"

    except requests.exceptions.Timeout:
        return "Timeout"
    except requests.exceptions.ConnectionError:
        return "Connection error"
    except Exception as e:
        return f"Error: {e}"

def main():
    with open("config/websites.json") as f:
        data = json.load(f)

    for url in data["links_to_check"]:
        print(f"\n Checking: {url}")

        apis = detect_apis(url)

        if not apis:
            print("Not found any API endpoints.")
        else:
            for api in apis:
                api_url = api["url"]
                score = api["score"]

                print(f"\n - Endpoint: {api_url} (score: {score})")

                status = check_api_status(api_url)
                print(f"   Status: {status}")
    
    # API KEY
    # API_KEY = ""

    # genai.configure(api_key=API_KEY)

    # model = genai.GenerativeModel("gemini-2.5-flash")

    # response = model.generate_content("Hi")

    # print(response.text)

if __name__ == "__main__":
    main()