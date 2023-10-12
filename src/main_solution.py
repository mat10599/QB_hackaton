from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
import base64
from io import BytesIO

from utils.variables import DATA_PATH, MODEL_PATH


def generate_predictions(image, model_name: str = "model_vgg16.h5"):
    image = preprocess_image(image)
    model = load_model(model_name)
    pred = model.predict(image)
    return pred


def preprocess_image(image):
    
    decoded = base64.b64decode(image)
    image = Image.open(BytesIO(decoded))
    image = image.convert('RGB')
    image = image.resize((64, 64))
    image = np.array(image) / 255.0  # Rescale pixel values to [0, 1]
    image = np.reshape(image, (1, 64, 64, 3))
    return image


def load_model(model_file):
    model_path = MODEL_PATH / model_file
    model = tf.keras.models.load_model(model_path)
    return model

############# TESTS #############
# generate_predictions(DATA_PATH/"test_data"/"images" /
#                      "20230314_methane_mixing_ratio_id_2274.tif")
