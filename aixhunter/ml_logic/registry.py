import os

import tensorflow as tf
from google.cloud import storage


def save_results(params: dict, metrics: dict) -> None:
    """
    Persist params & metrics locally on the hard drive at
    "{LOCAL_REGISTRY_PATH}/params/{current_timestamp}.pickle"
    "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    - (unit 03 only) if MODEL_TARGET='mlflow', also persist them on MLflow
    """
    pass

def save_model(model: tf.keras.Model) -> None:
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on MLflow instead of GCS (for unit 0703 only) --> unit 03 only
    """

    pass


def save_model(model:tf.keras.Model, name:str) -> None:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """
    model.save(f"./model/{name}" + '.h5')
    return None

def load_latest_model() -> tf.keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """
    # Look for latest model on gcs
    storage_client = storage.Client()
    model_bucket = 'dn_model'
    blob_list = [(blob, blob.updated) for blob in storage_client.list_blobs(model_bucket)]
    latest_model_name = sorted(blob_list, key=lambda tup: tup[1])[-1][0].name

    model_path = os.path.join(os.path.expanduser('~'), "code", "MyThunder11", "aixhunter", "models")
    model_file = os.path.join(model_path, latest_model_name)

    if not os.path.isfile(model_file):
        print('Uploading latest model from gcs')
        bucket = storage_client.bucket(model_bucket)
        blob = bucket.blob(latest_model_name)
        blob.download_to_filename(model_file)
        print('Latest model downloaded')
    else:
        print('Loading model from cache')
    model = tf.keras.models.load_model(model_file)
    return model
