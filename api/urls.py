from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^faces/?$', Prediction.as_view(), name = 'faces prediction'),
    re_path(r'^general/?$', Prediction.as_view(), name = 'general prediction'),
]
