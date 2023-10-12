from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
import base64
from io import BytesIO

from utils.variables import DATA_PATH, MODEL_PATH


def generate_predictions(image, model_name: str = "model_vgg16.h5"):
    """generate predictions from the image

    Args:
        image (_type_): image to be predicted
        model_name (str, optional): model to use. Defaults to "model_vgg16.h5".

    Returns:
        np.array: predicted probability of plume
    """
    image = preprocess_image(image)
    model = load_model(model_name)
    pred = model.predict(image)
    return pred


def preprocess_image(image):
    """preprocess the image to be fed to the model

    Args:
        image (_type_): image to be preprocessed

    Returns:
        _type_: preprocessed image as an array of shape (1, 64, 64, 3)
    """
    
    decoded = base64.b64decode(image)
    image = Image.open(BytesIO(decoded))
    image = image.convert('RGB')
    image = image.resize((64, 64))
    image = np.array(image) / 255.0  # Rescale pixel values to [0, 1]
    image = np.reshape(image, (1, 64, 64, 3))
    return image


def load_model(model_file):
    """load the model

    Args:
        model_file (str): model name

    Returns:
        tf.keras.models: model
    """
    model_path = MODEL_PATH / model_file
    model = tf.keras.models.load_model(model_path)
    return model

