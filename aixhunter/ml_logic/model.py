import numpy as np
import time
import datetime
from typing import Tuple
from aixhunter.params import *
import tensorflow as tf



from registry import save_model
from data import load_images_from_bucket


def load_model_VGG16():
    model = tf.keras.applications.VGG16(
        weights='imagenet',  # Load weights pre-trained on ImageNet.
        input_shape=(32, 32, 3),
        include_top=False
        )  # Do not include the ImageNet classifier at the top.
    return model


def set_nontrainable_layers(model):
    model.trainable = False
    return model


def add_last_layers(model):
    '''Take a pre-trained model, set its parameters as non-trainable, and add additional trainable layers on top'''
    rescale_layer = tf.keras.layers.Rescaling(1./255, input_shape=(32, 32, 3))
    base_model = set_nontrainable_layers(model)
    flatten_layer = tf.keras.layers.Flatten()
    dense_layer = tf.keras.layers.Dense(500, activation='relu')
    prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')


    model = tf.keras.models.Sequential([
        rescale_layer,
        base_model,
        flatten_layer,
        dense_layer,
        prediction_layer
    ])
    return model



def build_model():
    model = load_model_VGG16()
    model = add_last_layers(model)

    adam = tf.keras.optimizers.Adam(learning_rate=1e-4)

    model.compile(
        optimizer=adam,
        loss='binary_crossentropy',
        metrics=['accuracy', 'Precision', 'Recall']
    )

    return model



def train_model(
        train_dataset,
        val_dataset,
        epochs=10,
        batch_size=2,
        patience=5
        ):
    es = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=patience,
        restore_best_weights=True,
        )

    # Only load to cache batch n+1
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_dataset.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_dataset.cache().prefetch(buffer_size=AUTOTUNE)


    model = build_model()

    print('✅ Model compiled \nFitting Model')

    history = model.fit(train_ds,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=val_ds,
        callbacks=[es],
        verbose=1
        )

    print('✅ Model fitted, saving model')

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    save_model(model, f"model_{timestamp}.h5")

    """ save_results() # Insert metrics saving here"""
    return model, history


def evaluate_model(
        model: tf.keras.Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ) -> Tuple[tf.keras.Model, dict]:
    """
    Evaluate trained model performance on the dataset
    """


    return None

if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    train_ds = load_images_from_bucket(BUCKET_IMAGES)
    val_ds = load_images_from_bucket(BUCKET_IMAGES)
    train_model(train_ds, val_ds)
