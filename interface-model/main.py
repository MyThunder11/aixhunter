import os
import tensorflow as tf
import Path
import validators

from ..ml_logic import registry

def train():
    pass

def evaluate():

    pass

def pred(model:tf.keras.Model, img_path:Path) -> tuple[float, float]:
    """Returns a score and confidence interval based on the model and a url / path"""
    model = registry.load_model()
    if validators.url(img_path):
        img_path = tf.keras.utils.get_file(origin=img_path)
    else:
        assert os.path.isfile(img_path)

    img = tf.keras.utils.load_img(img_path, target_size=(256, 256))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.sigmoid(predictions[0])
    return predictions[0], score




if __name__ == '__main__':
    #preprocess()
    #train()
    #evaluate()
    #pred()
    pass
