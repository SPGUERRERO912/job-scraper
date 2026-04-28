from playwright.sync_api import sync_playwright

def capture_endpoints(url):
    endpoints = set()

    def handle_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            endpoints.add(request.url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("request", handle_request)
        page.goto(url)
        page.wait_for_timeout(5000)

        browser.close()

    return endpoints


