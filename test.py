# # #!/usr/bin/env python3
# # import requests
# # import time
# # import concurrent.futures
# # import argparse
# # import json
# # import csv
# # from urllib.parse import urljoin
# # import os

# # def create_shortened_url(base_url, long_url):
# #     """Create a shortened URL and return the short URL and ID"""
# #     endpoint = urljoin(base_url, '/api/shorten')
# #     response = requests.post(endpoint, json={'url': long_url})
# #     if response.status_code == 200:
# #         data = response.json()
# #         short_url = data['short_url']
# #         # Extract short_id from the short_url
# #         short_id = short_url.rstrip('/').split('/')[-1]
# #         return short_url, short_id
# #     else:
# #         print(f"Error creating short URL for {long_url}: {response.status_code}, {response.text}")
# #         return None, None

# # def verify_redirect(short_url, expected_long_url):
# #     """Verify that the short URL redirects to the expected long URL"""
# #     try:
# #         response = requests.get(short_url, allow_redirects=False)
# #         if response.status_code in [301, 302, 303, 307, 308]:
# #             redirect_url = response.headers.get('Location')
# #             if expected_long_url.startswith(redirect_url) or redirect_url.startswith(expected_long_url):
# #                 return True
# #             else:
# #                 print(f"Redirect mismatch: got {redirect_url}, expected {expected_long_url}")
# #                 return False
# #         else:
# #             print(f"Error verifying redirect for {short_url}: {response.status_code}")
# #             return False
# #     except requests.exceptions.RequestException as e:
# #         print(f"Request exception when verifying {short_url}: {e}")
# #         return False

# # def check_pod_info(base_url):
# #     """Get pod information from the /pod-info endpoint"""
# #     endpoint = urljoin(base_url, '/pod-info')
# #     try:
# #         response = requests.get(endpoint)
# #         if response.status_code == 200:
# #             return response.json()
# #         else:
# #             print(f"Error getting pod info: {response.status_code}, {response.text}")
# #             return None
# #     except requests.exceptions.RequestException as e:
# #         print(f"Request exception when checking pod info: {e}")
# #         return None

# # def delete_short_url(base_url, short_id):
# #     """Delete a shortened URL"""
# #     endpoint = urljoin(base_url, f'/api/delete/{short_id}')
# #     try:
# #         response = requests.delete(endpoint)
# #         if response.status_code == 200:
# #             return True
# #         else:
# #             print(f"Error deleting short URL {short_id}: {response.status_code}, {response.text}")
# #             return False
# #     except requests.exceptions.RequestException as e:
# #         print(f"Request exception when deleting {short_id}: {e}")
# #         return False

# # # def create_multiple_urls(base_url, num_urls, concurrent=5):
# # #     """Create multiple shortened URLs using a thread pool"""
# # #     test_urls = [f"https://example.com/testpage{i}" for i in range(num_urls)]
# # #     created_urls = []
    
# # #     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
# # #         # Create a future for each URL creation
# # #         future_to_url = {executor.submit(create_shortened_url, base_url, url): url for url in test_urls}
        
# # #         for future in concurrent.futures.as_completed(future_to_url):
# # #             long_url = future_to_url[future]
# # #             try:
# # #                 short_url, short_id = future.result()
# # #                 if short_url:
# # #                     created_urls.append({
# # #                         'long_url': long_url,
# # #                         'short_url': short_url,
# # #                         'short_id': short_id
# # #                     })
# # #             except Exception as e:
# # #                 print(f"Error creating short URL for {long_url}: {e}")
    
# # #     return created_urls

# # def create_multiple_urls(base_url, num_urls, concurrent_threads=5):
# #     """Create multiple shortened URLs using a thread pool."""
# #     test_urls = [f"https://example.com/testpage{i}" for i in range(num_urls)]
# #     created_urls = []
    
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_threads) as executor:
# #         future_to_url = {executor.submit(create_shortened_url, base_url, url): url for url in test_urls}
        
# #         for future in concurrent.futures.as_completed(future_to_url):
# #             long_url = future_to_url[future]
# #             try:
# #                 short_url, short_id = future.result()
# #                 if short_url:
# #                     created_urls.append({
# #                         'long_url': long_url,
# #                         'short_url': short_url,
# #                         'short_id': short_id
# #                     })
# #             except Exception as e:
# #                 print(f"Error creating short URL for {long_url}: {e}")
    
# #     return created_urls

# # def verify_multiple_redirects(created_urls, concurrent=5):
# #     """Verify multiple redirects using a thread pool"""
# #     results = []
    
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
# #         # Create a future for each redirect verification
# #         future_to_url = {executor.submit(verify_redirect, url_info['short_url'], url_info['long_url']): url_info 
# #                          for url_info in created_urls}
        
# #         for future in concurrent.futures.as_completed(future_to_url):
# #             url_info = future_to_url[future]
# #             try:
# #                 success = future.result()
# #                 results.append({
# #                     **url_info,
# #                     'redirect_success': success
# #                 })
# #             except Exception as e:
# #                 print(f"Error verifying redirect for {url_info['short_url']}: {e}")
# #                 results.append({
# #                     **url_info,
# #                     'redirect_success': False
# #                 })
    
# #     return results

# # def check_pod_distribution(base_url, num_requests, concurrent=10):
# #     """Make multiple requests to check pod distribution"""
# #     pod_results = []
    
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
# #         # Create a future for each pod info request
# #         futures = [executor.submit(check_pod_info, base_url) for _ in range(num_requests)]
        
# #         for future in concurrent.futures.as_completed(futures):
# #             try:
# #                 pod_info = future.result()
# #                 if pod_info:
# #                     pod_results.append(pod_info)
# #             except Exception as e:
# #                 print(f"Error checking pod info: {e}")
    
# #     return pod_results

# # def delete_multiple_urls(base_url, url_infos, concurrent=5):
# #     """Delete multiple shortened URLs using a thread pool"""
# #     results = []
    
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
# #         # Create a future for each URL deletion
# #         future_to_url = {executor.submit(delete_short_url, base_url, url_info['short_id']): url_info 
# #                          for url_info in url_infos}
        
# #         for future in concurrent.futures.as_completed(future_to_url):
# #             url_info = future_to_url[future]
# #             try:
# #                 success = future.result()
# #                 results.append({
# #                     **url_info,
# #                     'delete_success': success
# #                 })
# #             except Exception as e:
# #                 print(f"Error deleting URL {url_info['short_id']}: {e}")
# #                 results.append({
# #                     **url_info,
# #                     'delete_success': False
# #                 })
    
# #     return results

# # def main():
# #     parser = argparse.ArgumentParser(description='Test URL shortener service')
# #     parser.add_argument('--base-url', required=True, help='Base URL of the URL shortener service')
# #     parser.add_argument('--num-urls', type=int, default=10, help='Number of URLs to create')
# #     parser.add_argument('--num-pod-requests', type=int, default=100, help='Number of pod info requests to make')
# #     parser.add_argument('--concurrent', type=int, default=10, help='Number of concurrent requests')
# #     parser.add_argument('--output-dir', default='./test_results', help='Directory for output files')
# #     parser.add_argument('--no-cleanup', action='store_true', help='Do not delete created URLs after testing')
# #     args = parser.parse_args()

# #     base_url = args.base_url.rstrip('/')
    
# #     # Create output directory if it doesn't exist
# #     os.makedirs(args.output_dir, exist_ok=True)
    
# #     # 1. Create multiple shortened URLs
# #     print(f"Creating {args.num_urls} shortened URLs with {args.concurrent} concurrent requests...")
# #     start_time = time.time()
# #     created_urls = create_multiple_urls(base_url, args.num_urls, args.concurrent)
# #     create_time = time.time() - start_time
# #     print(f"Created {len(created_urls)} shortened URLs in {create_time:.2f} seconds")
    
# #     # Save created URLs to a file
# #     created_urls_file = os.path.join(args.output_dir, 'created_urls.json')
# #     with open(created_urls_file, 'w') as f:
# #         json.dump(created_urls, f, indent=2)
# #     print(f"Created URLs saved to {created_urls_file}")
    
# #     # 2. Verify redirects
# #     print(f"\nVerifying {len(created_urls)} redirects...")
# #     start_time = time.time()
# #     redirect_results = verify_multiple_redirects(created_urls, args.concurrent)
# #     redirect_time = time.time() - start_time
    
# #     redirect_success = sum(1 for result in redirect_results if result.get('redirect_success', False))
# #     print(f"Successfully verified {redirect_success}/{len(redirect_results)} redirects in {redirect_time:.2f} seconds")
    
# #     # Save redirect results to a file
# #     redirect_results_file = os.path.join(args.output_dir, 'redirect_results.json')
# #     with open(redirect_results_file, 'w') as f:
# #         json.dump(redirect_results, f, indent=2)
# #     print(f"Redirect results saved to {redirect_results_file}")
    
# #     # 3. Check pod load distribution
# #     print(f"\nMaking {args.num_pod_requests} requests to check pod distribution...")
# #     start_time = time.time()
# #     pod_results = check_pod_distribution(base_url, args.num_pod_requests, args.concurrent)
# #     pod_time = time.time() - start_time
    
# #     pod_counts = {}
# #     for result in pod_results:
# #         pod_name = result['pod_name']
# #         pod_counts[pod_name] = pod_counts.get(pod_name, 0) + 1
    
# #     print(f"Completed {len(pod_results)}/{args.num_pod_requests} pod info requests in {pod_time:.2f} seconds")
# #     print("\nPod request distribution:")
# #     for pod, count in pod_counts.items():
# #         print(f"  {pod}: {count} requests ({count/len(pod_results)*100:.1f}%)")
    
# #     # Save pod results to a file
# #     pod_results_file = os.path.join(args.output_dir, 'pod_results.json')
# #     with open(pod_results_file, 'w') as f:
# #         json.dump(pod_results, f, indent=2)
# #     print(f"Pod results saved to {pod_results_file}")
    
# #     # Create a summary report
# #     summary_file = os.path.join(args.output_dir, 'summary.csv')
# #     with open(summary_file, 'w', newline='') as csvfile:
# #         writer = csv.writer(csvfile)
# #         writer.writerow(['Test', 'Success', 'Total', 'Percentage', 'Time (s)'])
# #         writer.writerow(['URL Creation', len(created_urls), args.num_urls, 
# #                         f"{len(created_urls)/args.num_urls*100:.1f}%", f"{create_time:.2f}"])
# #         writer.writerow(['Redirect Verification', redirect_success, len(redirect_results), 
# #                         f"{redirect_success/len(redirect_results)*100:.1f}%", f"{redirect_time:.2f}"])
# #         writer.writerow(['Pod Info Requests', len(pod_results), args.num_pod_requests, 
# #                         f"{len(pod_results)/args.num_pod_requests*100:.1f}%", f"{pod_time:.2f}"])
        
# #         writer.writerow([])
# #         writer.writerow(['Pod', 'Requests', 'Percentage'])
# #         for pod, count in pod_counts.items():
# #             writer.writerow([pod, count, f"{count/len(pod_results)*100:.1f}%"])
    
# #     print(f"Summary report saved to {summary_file}")
    
# #     # 4. Clean up - delete shortened URLs (unless --no-cleanup is specified)
# #     if not args.no_cleanup and created_urls:
# #         print(f"\nCleaning up - deleting {len(created_urls)} shortened URLs...")
# #         start_time = time.time()
# #         delete_results = delete_multiple_urls(base_url, created_urls, args.concurrent)
# #         delete_time = time.time() - start_time
        
# #         delete_success = sum(1 for result in delete_results if result.get('delete_success', False))
# #         print(f"Successfully deleted {delete_success}/{len(delete_results)} shortened URLs in {delete_time:.2f} seconds")
        
# #         # Save delete results to a file
# #         delete_results_file = os.path.join(args.output_dir, 'delete_results.json')
# #         with open(delete_results_file, 'w') as f:
# #             json.dump(delete_results, f, indent=2)
# #         print(f"Delete results saved to {delete_results_file}")
    
# #     print("\nTesting complete!")

# # if __name__ == "__main__":
# #     main()


# import requests

# BASE_URL = "http://127.0.0.1:57511"  # <-- Change this to your service URL

# sites = [
#     "https://leetcode.com",
#     "https://github.com",
#     "https://kubernetes.io",
#     "https://www.docker.com",
#     "https://www.perplexity.ai"
# ]

# shortened = {}

# print("Shortening URLs...")
# for site in sites:
#     resp = requests.post(f"{BASE_URL}/api/shorten", json={"url": site})
#     if resp.status_code == 200:
#         short_url = resp.json()["short_url"]
#         print(f"{site} -> {short_url}")
#         shortened[site] = short_url
#     else:
#         print(f"Failed to shorten {site}: {resp.text}")

# print("\nTesting redirects...")
# for site, short_url in shortened.items():
#     try:
#         r = requests.get(short_url, allow_redirects=False)
#         if r.status_code in (301, 302, 303, 307, 308):
#             location = r.headers.get("Location", "")
#             print(f"{short_url} redirects to {location} (expected: {site})")
#             if location.startswith(site):
#                 print("  ✅ Redirect OK")
#             else:
#                 print("  ❌ Redirect mismatch")
#         else:
#             print(f"{short_url} did not redirect, status: {r.status_code}")
#     except Exception as e:
#         print(f"Error testing {short_url}: {e}")


import requests
import concurrent.futures
import time

BASE_URL = "http://127.0.0.1:60999"  # <-- Change this to your service URL

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
