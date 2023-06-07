import requests
import json
import base64
from PIL import Image, JpegImagePlugin
import io


def post_test():
    # Load an image and convert it to base64
    with open("szAKSQPN.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    """ with open('base64.txt', 'r') as image_text:
        encoded_string = image_text.read() """

    # Specify the url of your Django server
    url = "http://localhost:8000"

    # Format the data as JSON
    data = json.dumps({"image": encoded_string})

    # Send a POST request to the server
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

    # Print out the response from the server
    print(response.content)
    imgdata = base64.b64decode(encoded_string.encode('utf-8'))
    Image.open(io.BytesIO(imgdata)).save('test.jpeg')




def decode_test():
    with open('base64.txt', 'r') as f:
        img_64 = f.read()
    imgdata = base64.b64decode(img_64)
    image = Image.open(io.BytesIO(imgdata))
    print(type(image))
    print(isinstance(image, JpegImagePlugin.JpegImageFile))

post_test()
