import requests
import time
from concurrent.futures import ThreadPoolExecutor

# define your URL
url = "http://34.163.252.117:8080"

# the URL to be sent in the POST data
scrape_url = 'https://miro.medium.com/v2/resize:fit:1400/0*EAwg7WIIMhgnSfLf.png'

# define how to send a request
def send_post():
    response = requests.post(url, data={'url': scrape_url})
    return response.content

# define how many requests you want to send at the same time
num_requests = 100


start_time = time.time()
# create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_requests) as executor:
    futures = {executor.submit(send_post) for _ in range(num_requests)}
end_time = time.time()


# print the results
for future in futures:
    print(future.result())

print(f"Sent {num_requests} requests in {end_time - start_time} seconds")
