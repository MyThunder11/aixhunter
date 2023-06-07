import os
import joblib
from django.apps import AppConfig
from django.conf import settings



class ApiConfig(AppConfig):
    name = 'model'
    MODEL_FILE = os.listdir(settings.MODELS)
    model = joblib.load(MODEL_FILE)


""" class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api' """

inst = ApiConfig()
print(settings.BASE_DIR)
print(inst.model)
