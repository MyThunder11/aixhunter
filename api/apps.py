import os
import joblib
from django.apps import AppConfig
from django.conf import settings
from aixhunter.ml_logic.registry import load_latest_model
from aixhunter.params import *


class ApiConfig(AppConfig):
    name = 'aixhunter'
    model_faces = load_latest_model(BUCKET_FACE_MODELS)
    model_general = load_latest_model(BUCKET_GENERAL_MODELS)



""" class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api' """
