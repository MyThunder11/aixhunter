import os
import joblib
from django.apps import AppConfig
from django.conf import settings
from aixhunter.ml_logic.registry import load_latest_model



class ApiConfig(AppConfig):
    name = 'model'
    model = load_latest_model()


""" class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api' """

inst = ApiConfig()
print(settings.BASE_DIR)
print(inst.model)
