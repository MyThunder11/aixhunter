import numpy as np
import pandas as pd
from PIL import Image
import io
from .apps import *
from aixhunter.interface_model.main import pred
from rest_framework.views import APIView
from rest_framework.response import Response
import base64
import json
import requests
import validators



class Prediction(APIView):
    def post(self, request):
        """Return prediction file format through POST.
        The incoming POST request can be one of the following:
        - An image file
        - A base64 image (either raw or with html tags)
        - A URL pointing to an image
        """
        allowed_extensions = ['.jpg', '.jpeg', '.jpe', '.png', '.bmp', '.gif']
        # If the request contains an image file
        if 'file' in request.FILES:
            image = request.FILES.get('file')
            try:
                # Get the file extension of the image
                file_extension = os.path.splitext(image.name)[1]
                if file_extension.lower() not in allowed_extensions:
                    return Response({'error': f'file format not supported, please use one of {allowed_extensions}'}, status=400)
                path = f'temp{file_extension}'
                # Save the image locally
                with open(path, 'wb') as saved_file:
                    saved_file.write(image.read())
                print('image saved locally')
            except Exception as e:
                # Return an error response if there's any exception
                return Response({'error': str(e)}, status=400)

        # If the request contains a URL
        elif 'url' in request.data:
            data = request.data.get('url')
            # If the URL is valid
            if validators.url(data):
                try:
                    path = data
                    # Test the url for forbidden
                    response = requests.get(path)
                    response.raise_for_status()
                    img_data = response.content
                except requests.exceptions.RequestException as e:
                    # Return an error response if there's any exception
                    return Response({'error': str(e)}, status=400)

                try:
                    # Check for file extension
                    file_extension = os.path.splitext(response.url)[1]
                    file_extension = '.jpeg' if file_extension == '' else file_extension
                    assert file_extension.lower() in allowed_extensions
                except:
                    return Response({'error': f'file format not supported, please use one of {allowed_extensions}'}, status=400)
                #Write image
                path = f'temp{file_extension}'
                with open(path, 'wb') as handler:
                    handler.write(img_data)
            else:
                # If the request contains a base64 image
                base64_image = request.data.get('url')
                if base64_image is None:
                    return Response({'error': 'No image found'}, status=400)
                try:
                    # If the base64 image string has a comma, take everything after it
                    base64_image = base64_image.split(',')[1] if ',' in base64_image else base64_image
                    # Decode the base64 image string into bytes
                    imgdata = base64.b64decode(base64_image)
                    # Convert the bytes into an image
                    image = Image.open(io.BytesIO(imgdata))
                    # Get the format of the image (e.g. 'png', 'jpg')
                    file_extension =  '.' + image.format.lower()
                    # Save the image locally
                    path = f'temp{file_extension}'
                    image.save(path)
                    if file_extension.lower() not in allowed_extensions:
                        return Response({'error': f'file format not supported, please use one of {allowed_extensions}'}, status=400)
                except Exception as e:
                    # Return an error response if there's any exception
                    return Response({'error': str(e)}, status=400)
        try:
            Image.open(path).verify()
        except Exception as e:
            return Response({"Invalid image": str(e)[:-12]})
        # Make a prediction using the model
        score = pred(ApiConfig.model , path)
        # If the score is 0.99 or higher, the prediction is 1; otherwise, it's 0
        prediction = 1 if score >= 0.99 else 0
        # Prepare the response dictionary
        response_dict = {"Prediction": prediction, "Score": score}
        print(response_dict)
        # Return the response dictionary
        return Response(response_dict, status=200)



    def get(self, request):
        """Return prediction file format through GET.
        The incoming GET request should contain a URL pointing to an image.
        """
        allowed_extensions = ['.jpg', '.jpeg', '.jpe', '.png', '.bmp', '.gif']
        try:
            # Get the URL from the request
            image_url = request.GET.get('url')
            # Make a GET request to the URL
            response = requests.get(image_url)
            response.raise_for_status()
            img_data = response.content
        except requests.exceptions.RequestException as e:
            # Return an error response if there's any exception
            return Response({'error': str(e)}, status=400)

        try:
            # Check for file extension
            file_extension = os.path.splitext(response.url)[1]
            file_extension = '.jpeg' if file_extension == '' else file_extension
            assert file_extension.lower() in allowed_extensions
        except:
            return Response({'error': f'file format not supported, please use one of {allowed_extensions}'}, status=400)
        #Write image
        path = f'temp{file_extension}'
        with open(path, 'wb') as handler:
            handler.write(img_data)
        try:
            Image.open(path).verify()
        except Exception as e:
            return Response({"Invalid image": str(e)[:-12]})
        # Use the model to make a prediction
        model = ApiConfig.model
        score = pred(model, image_url)
        prediction = 1 if score >= 0.99 else 0
        response_dict = {"Prediction": prediction, "Score": score}
        print(response_dict)
        return Response(response_dict, status=200)
