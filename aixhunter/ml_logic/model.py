import numpy as np
import time
import datetime
from typing import Tuple
from aixhunter.params import *
import tensorflow as tf

from aixhunter.ml_logic.data import load_images_from_bucket


def load_model():
    model = tf.keras.applications.ConvNeXtBase(
        include_top=False,
        weights="imagenet",
        input_shape=(200, 200, 3),
    )
    model.trainable = False
    return model


def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(200, 200, 3)),
        load_model(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
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
