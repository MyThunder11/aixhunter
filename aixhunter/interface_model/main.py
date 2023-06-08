import os
import tensorflow as tf
import validators
from pathlib import Path
from PIL import Image, JpegImagePlugin

from aixhunter.ml_logic import registry

def train():
    pass

def evaluate():

    pass

def pred(model:tf.keras.Model, img_path:Path) -> float:
    """Returns a score and confidence interval based on the model and a url / path"""
    if validators.url(img_path):
        img_path = tf.keras.utils.get_file(origin=img_path)
    img = tf.keras.utils.load_img(img_path, target_size=(256, 256))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    return float(predictions)




if __name__ == '__main__':
    #preprocess()
    #train()
    #evaluate()
    model = registry.load_latest_model()
    print(pred(model, ''))
