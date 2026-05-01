import requests

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
    
def analyze_api_endpoints(endpoints):
    results = []
    for api in endpoints:
        url = api["url"]
        score = api["score"]
        status = check_api_status(url)

        results.append({
            "url": url,
            "score": score,
            "status": status
        })
    
    return results