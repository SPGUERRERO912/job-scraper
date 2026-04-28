from endpoint_analyzer.capture_endpoints import capture_endpoints

if __name__ == "__main__":
    url = "https://careers.astrazeneca.com/location/costa-rica-jobs/7684/3624060/2"
    endpoints = capture_endpoints(url)

    for e in endpoints:
        print(e)