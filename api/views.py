import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from .apps import *
from aixhunter.interface_model.main import pred
from rest_framework.views import APIView
from rest_framework.response import Response
import base64




class Prediction(APIView):
    def post(self, request):
        print(request)
        if request.method == 'POST':
            model = ApiConfig.model
            prediction, score = pred(model, data)
            response_dict = {"Prediction": prediction, "Score": score}
            print(response_dict)
            return Response(response_dict, status=200)

    def get(self, request):
        print(request)
        if request.method == 'GET':
            # If given with url --> Tensorflow accpts urls
            if request.GET.get('method') == 'url':
                image = request.GET.get('url')
            # If given in Base64 --> provide image
            elif request.GET.get('method') == 'b64':
                b64_img = request.GET.get('data')
                image = Image.open(BytesIO(base64.b64decode(b64_img)))
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
