import numpy as np
import pandas as pd
from .apps import *
from aixhunter.ml_logic import pred
from rest_framework.views import APIView
from rest_framework.response import Response


class Prediction(APIView):
    def post(self, request):
        data = request.data
        model = ApiConfig.model
        #predict using independent variables
        PredictionMade = dtree.predict([[age, gender, cholesterol, bp, salt]])
        response_dict = {"Predicted drug": PredictionMade}
        print(response_dict)
        return Response(response_dict, status=200)
