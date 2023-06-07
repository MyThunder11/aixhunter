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




class Prediction(APIView):
    def post(self, request):
        data = json.loads(request.body)
        print(type(data['image']))
        base64_image = data['image']  # 'image' is the key in the JSON object
        if base64_image is None:
            return Response({'error': 'No image found'}, status=400)
        try:
            # base64_image = base64_image.split(',')[1]
            imgdata = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(imgdata))
            image.save('test.jpeg')
            path = 'test.jpeg'
            score = pred(ApiConfig.model , path)
            prediction = 1 if score >= 0.99 else 0
            response_dict = {"Prediction": prediction, "Score": score}
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        return Response(response_dict, status=200)

    def get(self, request):
        # If given with url --> Tensorflow accpts urls
        if request.GET.get('method') == 'url':
            image = request.GET.get('url')
        # If given in Base64 --> provide image
        elif request.GET.get('method') == 'file':
            pass
        else:
            return Response(status=400)
        model = ApiConfig.model
        score = pred(model, image)
        prediction = 1 if score >= 0.99 else 0
        response_dict = {"Prediction": prediction, "Score": score}
        print(response_dict)
        return Response(response_dict, status=200)
