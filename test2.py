import requests
import time
from concurrent.futures import ThreadPoolExecutor

# define your URL
url = "https://testing-fwbq4znlpq-od.a.run.app/api/general"

# the URL to be sent in the POST data
scrape_url = 'https://miro.medium.com/v2/resize:fit:1400/0*EAwg7WIIMhgnSfLf.png'

# define how to send a request
def send_post():
    response = requests.post(url, data={'url': scrape_url})
    return response.content

def post_img_test(url):
    # Send a POST request to the server
    response = requests.post(url, files={'file': open("szAKSQPN.jpg", "rb")})
    # Print out the response from the server
    return response.content

# define how many requests you want to send at the same time
num_requests = 100


start_time = time.time()
# create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_requests) as executor:
    futures = {executor.submit(post_img_test, url) for _ in range(num_requests)}
end_time = time.time()


# print the results
for future in futures:
    print(future.result())

print(f"Sent {num_requests} requests in {end_time - start_time} seconds")
