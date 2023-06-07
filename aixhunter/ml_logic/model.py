import numpy as np
import time
import datetime
from tensorflow import keras
from keras import layers, models, optimizers
from colorama import Fore, Style
from typing import Tuple

# Timing the TF import
print(Fore.BLUE + "\nLoading TensorFlow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow import keras
from keras import Model, Sequential, layers, regularizers, optimizers
from keras.callbacks import EarlyStopping

from registry import save_model

end = time.perf_counter()
print(f"\n✅ TensorFlow loaded ({round(end - start, 2)}s)")


def load_model_VGG16():
    model = keras.applications.VGG16(
        weights='imagenet',  # Load weights pre-trained on ImageNet.
        input_shape=(256, 256, 3),
        include_top=False
        )  # Do not include the ImageNet classifier at the top.
    return model


def set_nontrainable_layers(model):
    model.trainable = False
    return model


def add_last_layers(model):
    '''Take a pre-trained model, set its parameters as non-trainable, and add additional trainable layers on top'''
    rescale_layer = layers.Rescaling(1./255, input_shape=(256, 256, 3))
    base_model = set_nontrainable_layers(model)
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(500, activation='relu')
    prediction_layer = layers.Dense(1, activation='sigmoid')


    model = models.Sequential([
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

    adam = optimizers.Adam(learning_rate=1e-4)

    model.compile(
        optimizer=adam,
        loss='binary_crossentropy',
        metrics=['accuracy', 'Precision', 'Recall']
    )
    return model



def train_model(
        train_dataset,
        val_dataset,
        epochs=100,
        batch_size=32,
        patience=5
        ):
    es = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=patience,
        restore_best_weights=True,
        )

    model = build_model()

    history = model.fit(
        train_dataset,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=val_dataset,
        callbacks=[es]
        )

    accuracy = round(history.history['val_accuracy'][-1], 2)

    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    save_model(model, f"model_{accuracy}_{date}")

    return model, history


def evaluate_model(
        model: Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ) -> Tuple[Model, dict]:
    """
    Evaluate trained model performance on the dataset
    """


    return None

if __name__ == '__main__':
    model = build_model()
    print(model)
