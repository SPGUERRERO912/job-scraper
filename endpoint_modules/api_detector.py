from playwright.sync_api import sync_playwright
import json

STRONG_SIGNALS = [
    "jobs",
    "search",
    "positions",
    "openings"
]

WEAK_SIGNALS = [
    "job",
    "career",
    "position",
    "api"
]

NOISE = [
    "analytics",
    "track",
    "consent",
    "config",
    "image",
    "translation",
    "label",
    "locale",
    "widget",
    "cdn",
    "asset"
]

def score_url(url: str) -> int:
    url = url.lower()
    score = 0

    if any(n in url for n in NOISE):
        return -10

    score += sum(3 for s in STRONG_SIGNALS if s in url)
    score += sum(1 for s in WEAK_SIGNALS if s in url)

    if "search.json" in url:
        score += 5
    if "pcsx/search" in url:
        score += 5
    if "get-jobs" in url:
        score += 5
    if "/jobs" in url:
        score += 2

    return score

def detect_platform(url: str):
    url = url.lower()

    if "workday" in url and "/jobs" in url:
        return "workday"
    if "pcsx/search" in url:
        return "eightfold"
    if "search.json" in url:
        return "amazon_like"
    if "phenom" in url:
        return "phenom"

    return "unknown"

def is_candidate(url: str) -> bool:
    return score_url(url) >= 3

def score_response(data: dict) -> int:
    text = str(data).lower()
    signals = ["title", "job", "position", "location", "description"]
    return sum(1 for s in signals if s in text)


def detect_apis(url: str):
    results = []

    def handle_response(response):
        try:
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                return
            if not is_candidate(response.url):
                return

            data = response.json()
            score = score_response(data)

            if score >= 4:
                results.append({
                    "url": response.url,
                    "score": score,
                    "platform": detect_platform(response.url)
                })
        except:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-http2",
                "--disable-blink-features=AutomationControlled",  # FIX 1: hide automation flag
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )

        # FIX 2: use a realistic browser context with proper headers
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            viewport={"width": 1280, "height": 800},
        )

        page = context.new_page()
        page.on("response", handle_response)

        # FIX 3: try multiple wait strategies with graceful timeout fallback
        navigated = False
        for wait_until in ["domcontentloaded", "load", "commit"]:
            try:
                page.goto(url, wait_until=wait_until, timeout=60000)
                navigated = True
                break
            except Exception:
                pass

        if not navigated:
            browser.close()
            return []

        page.wait_for_timeout(4000)

        for _ in range(4):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        browser.close()

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results