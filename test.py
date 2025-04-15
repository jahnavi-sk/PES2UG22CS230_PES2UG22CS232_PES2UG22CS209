import requests
import concurrent.futures
import time

BASE_URL = "http://127.0.0.1:53641"  # <-- Change this to your service URL

sites = [
    "https://leetcode.com",
    "https://github.com",
    "https://kubernetes.io",
    "https://www.docker.com",
    "https://www.perplexity.ai"
]

shortened = {}

print("Shortening URLs...")
for site in sites:
    resp = requests.post(f"{BASE_URL}/api/shorten", json={"url": site})
    if resp.status_code == 200:
        short_url = resp.json()["short_url"]
        print(f"{site} -> {short_url}")
        shortened[site] = short_url
    else:
        print(f"Failed to shorten {site}: {resp.text}")

print("\nTesting redirects...")
for site, short_url in shortened.items():
    try:
        r = requests.get(short_url, allow_redirects=False)
        if r.status_code in (301, 302, 303, 307, 308):
            location = r.headers.get("Location", "")
            print(f"{short_url} redirects to {location} (expected: {site})")
            if location.startswith(site):
                print("  ✅ Redirect OK")
            else:
                print("  ❌ Redirect mismatch")
        else:
            print(f"{short_url} did not redirect, status: {r.status_code}")
    except Exception as e:
        print(f"Error testing {short_url}: {e}")


NUM_REQUESTS = 100  # Number of requests to make to test load balancing
CONCURRENT_REQUESTS = 10 # Number of concurrent requests

def get_pod_info():
    """
    Retrieves pod information from the /pod-info endpoint.
    """
    try:
        response = requests.get(f"{BASE_URL}/pod-info")
        if response.status_code == 200:
            return response.json()['pod_name']
        else:
            print(f"Error getting pod info: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return None

def make_requests(num_requests, concurrent_requests):
    """
    Makes multiple concurrent requests to the /pod-info endpoint to check load balancing.
    """
    pod_counts = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = [executor.submit(get_pod_info) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            pod_name = future.result()
            if pod_name:
                pod_counts[pod_name] = pod_counts.get(pod_name, 0) + 1
    return pod_counts

def main():
    """
    Main function to test load balancing.
    """
    start_time = time.time()
    pod_counts = make_requests(NUM_REQUESTS, CONCURRENT_REQUESTS)
    end_time = time.time()

    print("Pod request distribution:")
    total_requests = sum(pod_counts.values())
    for pod, count in pod_counts.items():
        percentage = (count / total_requests) * 100
        print(f"  {pod}: {count} requests ({percentage:.2f}%)")

    print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
