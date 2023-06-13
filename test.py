import requests
import json
import base64
from PIL import Image, JpegImagePlugin
import io


def post_b64_test():
    # Load an image and convert it to base64
    with open("szAKSQPN.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    encoded_string_2= "data:image/png;base64, " + encoded_string

    # Specify the url of your Django server
    url = "http://34.163.252.117:8080"

    # Format the data as JSON
    data = json.dumps({"url": encoded_string})
    data2 = json.dumps({'url': encoded_string_2})

    # Send a POST request to the server
    response = requests.post(url, data=data,  headers={'Content-Type': 'application/json'})
    response2 = requests.post(url, data=data2, headers={'Content-Type': 'application/json'})

    # Print out the response from the server
    return response.content, response.status_code, response2.content, response2.status_code

def post_img_test():
    # define URL
    url = "http://34.163.252.117:8080"

    # Send a POST request to the server
    response = requests.post(url, files={'file': open("szAKSQPN.jpg", "rb")})

    # Print out the response from the server
    return response.content

def post_url():
    # define URL
    url = "http://34.163.252.117:8080"

    scrape_url = 'https://miro.medium.com/v2/resize:fit:1400/0*EAwg7WIIMhgnSfLf.png'

    # Send a POST request to the server
    response = requests.post(url, data={'url':scrape_url})

    # Print out the response from the server
    return response.content

def post_non_image_url():
    # define URL
    url = "http://34.163.252.117:8080"

    scrape_url = 'https://www.geeksforgeeks.org/python-os-path-splitext-method/'

    # Send a POST request to the server
    response = requests.post(url, data={'url':scrape_url})

    # Print out the response from the server
    return response.content

def get_url():
    # define URL
    url = "http://34.163.252.117:8080"

    scrape_url = 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTaKwXwvWoHu-pc_K4jXH9JpA1KIvo21RYoWoUFpzZncXr6PzR8om5tr6R3CY77s1NzuVuH8ItRH9lSsRw'

    # Send a POST request to the server
    response = requests.get(url, params={'url':scrape_url})

    # Print out the response from the server
    return response.content



def test_forbidden():
    scrap_url = 'https://webtoon-phinf.pstatic.net/20230215_68/1676406944721ykbfR_JPEG/6HelloBaby_thumbnail_desktop.jpg?type=a210'
    url = "http://34.163.252.117:8080"
    response = requests.post(url,  data={'url': scrap_url})
    return response.content, response.status_code


def test_bad_url():
    scrap_url = 'iyfgskejbqsekjcbq:ekjcvb!lqdjnvc'
    url = "http://34.163.252.117:8080"
    response = requests.post(url,  data={'url': scrap_url})
    return response.content, response.status_code


print(post_img_test())
print(post_b64_test())
print(post_url())
print(get_url())
print(test_forbidden())
print(post_non_image_url())
print(test_bad_url())
