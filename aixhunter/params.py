import os
from pathlib import Path
import numpy as np

##################  VARIABLES  ##################
BUCKET_MODELS = 'dn_model'
BUCKET_IMAGES = 'aixhunter_data_general'
##################  CONSTANTS  ##################


##################  PATHS  ######################
BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_MODELS_REGISTRY = os.path.join(BASE_DIR, 'models')
