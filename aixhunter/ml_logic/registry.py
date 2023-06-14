import os
import time


import tensorflow as tf
from google.cloud import storage
from aixhunter.params import *
from aixhunter.ml_logic.model import build_model

def save_results(params: dict, metrics: dict) -> None:
    """
    Persist params & metrics locally on the hard drive at
    - (unit 03 only) if MODEL_TARGET='mlflow', also persist them on MLflow
    """

    pass


def save_model(model: tf.keras.Model, file_name:str) -> None:
    f"""
    Persist trained model locally on the hard drive in "{LOCAL_MODELS_REGISTRY}"
    - Persist in bucket on GCS at "{BUCKET_FACE_MODELS}/TIMESTAMP.h5"
    """

    # Save model locally
    model_path = os.path.join(LOCAL_MODELS_REGISTRY, file_name)
    model.save(model_path)  # Keras Method to save the model

    print("✅ Model saved locally")
    client = storage.Client()
    bucket = client.bucket(BUCKET_FACE_MODELS)
    blob = bucket.blob(f"{file_name}")
    blob.upload_from_filename(model_path)

    print("✅ Model saved to GCS")

    return None



def load_latest_model(bucket: str = BUCKET_FACE_MODELS) -> tf.keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """
    # Look for latest model on gcs
    storage_client = storage.Client()
    model_bucket = bucket
    blob_list = [(blob, blob.updated) for blob in storage_client.list_blobs(model_bucket)]
    latest_model_name = sorted(blob_list, key=lambda tup: tup[1])[-1][0].name

    model_name = 'face' if model_bucket == BUCKET_FACE_MODELS else 'general'

    print(f'Latest {model_name} model to be used: {latest_model_name}')
    model_path = os.path.join(os.getcwd(), "models")
    model_file = os.path.join(model_path, latest_model_name)
    lockfile = ".lock"
    while True:
        if not os.path.isfile(model_file):
            print('Uploading latest model from gcs')
            with open(lockfile, 'w') as file:
                file.write('')
            bucket = storage_client.bucket(model_bucket)
            blob = bucket.blob(latest_model_name)
            blob.download_to_filename(model_file)
            os.remove(lockfile)
            print(f'Latest {model_name} model downloaded')
            break
        else:
            if os.path.isfile(lockfile):
                print("Lockfile exists, waiting...")
                time.sleep(10)
            else:
                print(f'Loading {model_name} model from cache')
                break
    if model_bucket == BUCKET_FACE_MODELS:
        model = tf.keras.models.load_model(model_file)
    elif model_bucket == BUCKET_GENERAL_MODELS:
        model = build_model()
        model.load_weights(model_file)
    print(f"✅ {model_name.upper()} Model loaded")
    return model
