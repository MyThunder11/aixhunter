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



class Prediction(APIView):
    def post(self, request):
        if 'file' in request.FILES:
            image = request.FILES['file']
            try:
                file_extension = os.path.splitext(image.name)[1]
                path = f'temp{file_extension}'
                with open(path, 'wb') as saved_file:
                    saved_file.write(image.read())
                    print('image saved locally')
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            base64_image = request.data['image']  # 'image' is the key in the JSON object
            if base64_image is None:
                return Response({'error': 'No image found'}, status=400)
            try:
                # base64_image = base64_image.split(',')[1] # a rétintégrer en fonction du format reçu
                imgdata = base64.b64decode(base64_image)
                image = Image.open(io.BytesIO(imgdata))
                file_extension = image.format.lower()
                path = f'temp.{file_extension}'
                image.save(path)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        score = pred(ApiConfig.model , path)
        prediction = 1 if score >= 0.99 else 0
        response_dict = {"Prediction": prediction, "Score": score}
        return Response(response_dict, status=200)

    def get(self, request):
        # If given with url --> Tensorflow accepts urls
        try:
            image_url = request.GET.get('url')
            response = requests.get(image_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=400)
        model = ApiConfig.model
        score = pred(model, image_url)
        prediction = 1 if score >= 0.99 else 0
        response_dict = {"Prediction": prediction, "Score": score}
        print(response_dict)
        return Response(response_dict, status=200)
