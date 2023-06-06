import os
from multiprocessing import Pool
import cv2

from params import *

from tqdm import tqdm
import pandas as pd
import numpy as np
from pathlib import Path
from colorama import Fore, Style
from google.cloud import storage, exceptions

from tensorflow.keras.utils import image_dataset_from_directory
#from dotenv import load_dotenv

# load_dotenv()




def download_bucket_objects(bucket_name:str, local_path:Path) -> None:
    """ Download images from bucket into local directory"""
    command = "gsutil -m cp -n gs://{BUCKETNAME} {localpath}".format(bucketname = bucket_name, localpath = local_path)
    os.system(command)
    print(f"{bucket_name} downloaded into {local_path}")
    return None


def load_images_from_directory(dir_path, labels='inferred', label_mode='binary', image_size=(32, 32), batch_size=32):
    dataset = image_dataset_from_directory(
        directory=dir_path,
        labels=labels,
        label_mode=label_mode,
        image_size=image_size,
        batch_size=batch_size,
        shuffle=True
    )
    return dataset


def image_to_df(dir_path:Path, chunk_size :int =None, chunk_number :int =None) -> tuple[np.array, np.array]:
    """Convert image directory to arrays and target list"""
    image_files = [file for file in os.listdir(dir_path) if 'Zone' not in file] #remove Zone Identifiers (WSL specific)
    if chunk_size:
        image_files = image_files[chunk_number*chunk_size:chunk_size*(chunk_number+1)]

    for i, im in tqdm(enumerate(image_files)):
        path = dir_path + "/" + im
        image= cv2.imread(path)
        if i == 0:
            images= np.expand_dims(np.array(image, dtype= float), axis= 0)
        else:
            image= np.expand_dims(np.array(image, dtype= float), axis= 0)
            images= np.append(images, image, axis= 0)
    y = [0 if 'REAL' in dir_path else 1 for i in range(len(image_files))]
    y = np.array(y)
    return images, y


def save_df(images:np.array, y:np.array, dir_path:Path, chunk_number:int=None) -> None:
    """Save X_proc and y_proc locally and on google cloud storage"""

    chunk_number = chunk_number if chunk_number >= 0 else 'all'

    # Save Locally
    a = np.save(os.path.join(dir_path, f"X_proc_{chunk_number}"), images)
    b = np.save(os.path.join(dir_path, f"y_proc_{chunk_number}"), y)


    # Upload to gcs
    # Instantiates a client
    storage_client = storage.Client()
    bucket_name = BUCKET_NAME
    bucket = storage_client.bucket(bucket_name)

    # Creates new blob (or supercedes old one)
    blob_name = f"X_processed_{chunk_number}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(os.path.join(dir_path, f"X_proc_{chunk_number}.npy"))
    print(f'X_processed_{chunk_number} uploaded')

    # Creates new blob (or supercedes old one)
    blob_name = f"y_processed_{chunk_number}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(os.path.join(dir_path, f"y_proc_{chunk_number}.npy"))
    print(f'y_processed_{chunk_number} uploaded')
    return None


def get_data(bucket:str, blob:str, cache_path:Path) -> np.array:
    """Downloads a blob from the bucket. If already cached, takes it from cache"""
    if os.path.exists(cache_path):
        print('Loading from local file')
        arr = np.load(cache_path)
    else:
        print('Loading from Google Cloud Storage')
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(blob)
        blob.download_to_filename(cache_path)
        arr = np.load(cache_path)
    print('Data loaded')
    return arr



filepath_images = os.path.join(os.path.expanduser('~'), "code", "MyThunder11", "aixhunter", "data", "raw")
filepath_processed = os.path.join(os.path.expanduser('~'), "code", "MyThunder11", "aixhunter", "data", "processed", "REAL")


""" for i in range(50):
    images, y = image_to_df(filepath_images, 1000, i)
    save_df(images, y, filepath_processed, 1000, i)
 """

load_images_from_directory(filepath_images)
