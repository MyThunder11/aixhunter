import requests
import json
import base64
from PIL import Image, JpegImagePlugin
import io


def post_img_test(url):
    # Send a POST request to the server
    response = requests.post(url, files={'file': open("szAKSQPN.jpg", "rb")})
    # Print out the response from the server
    return response.content

def post_b64_test(url):
    # Load an image and convert it to base64
    with open("szAKSQPN.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    encoded_string_2= "data:image/png;base64, " + encoded_string
    # Format the data as JSON
    data = json.dumps({"url": encoded_string})
    data2 = json.dumps({'url': encoded_string_2})
    # Send a POST request to the server with and without the html prefix
    response = requests.post(url, data=data,  headers={'Content-Type': 'application/json'})
    response2 = requests.post(url, data=data2, headers={'Content-Type': 'application/json'})

    # Print out the response from the server
    return response.content, response.status_code, response2.content, response2.status_code

def post_url(url):
    scrape_url = 'https://miro.medium.com/v2/resize:fit:1400/0*EAwg7WIIMhgnSfLf.png'
    # Send a POST request to the server
    response = requests.post(url, data={'url':scrape_url})
    # Print out the response from the server
    return response.content

def post_non_image_url(url):
    scrape_url = 'https://www.geeksforgeeks.org/python-os-path-splitext-method/'
    # Send a POST request to the server
    response = requests.post(url, data={'url':scrape_url})
    # Print out the response from the server
    return response.content

def get_url(url):
    scrape_url = 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTaKwXwvWoHu-pc_K4jXH9JpA1KIvo21RYoWoUFpzZncXr6PzR8om5tr6R3CY77s1NzuVuH8ItRH9lSsRw'
    # Send a POST request to the server
    response = requests.get(url, params={'url':scrape_url})
    # Print out the response from the server
    return response.content



def test_forbidden(url):
    scrape_url = 'https://webtoon-phinf.pstatic.net/20230215_68/1676406944721ykbfR_JPEG/6HelloBaby_thumbnail_desktop.jpg?type=a210'
    response = requests.post(url,  data={'url': scrape_url})
    return response.content, response.status_code


def test_bad_url(url):
    scrape_url = 'iyfgskejbqsekjcbq:ekjcvb!lqdjnvc'
    response = requests.post(url,  data={'url': scrape_url})
    return response.content, response.status_code



if __name__ == '__main__':
    urls = ['https://production-fwbq4znlpq-od.a.run.app/api/faces', 'https://production-fwbq4znlpq-od.a.run.app/api/general']
    for url in urls:
        print(url)
        print(post_img_test(url))
        print(post_b64_test(url))
        print(post_url(url))
        print(get_url(url))
        print(test_forbidden(url))
        print(post_non_image_url(url))
        print(test_bad_url(url))
