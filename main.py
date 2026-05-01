import json
from endpoint_modules.api_detector import detect_apis
from endpoint_modules.api_analyzer import analyze_api_endpoints
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def main():
    # with open("config/websites.json") as f:
    #     data = json.load(f)

    # for url in data["links_to_check"]:
    #     print(f"\n Checking: {url}")

    #     apis = detect_apis(url)

    #     if not apis:
    #         print("Not found any API endpoints.")
    #     else:
    #         print(f"Found {len(apis)} candidate API endpoints. Analyzing...")
    #         results = analyze_api_endpoints(apis)

    #         for res in results:
    #             print(f"URL: {res['url']}\nScore: {res['score']}\nStatus: {res['status']}\n")
    
    # API KEY
    # API_KEY = ""

    # genai.configure(api_key=API_KEY)

    # model = genai.GenerativeModel("gemini-2.5-flash")

    # response = model.generate_content("Hi")

    # print(response.text)

if __name__ == "__main__":
    main()