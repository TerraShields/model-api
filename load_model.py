import tensorflow_hub as hub
import tensorflow as tf
from __main__ import app
from PIL import Image
import numpy as np

custom_objects = {"KerasLayer": hub.KerasLayer}

model_classification = tf.keras.models.load_model(
    app.config['MODEL_PATH'], compile=False, custom_objects=custom_objects)

model_wind_spread = tf.keras.models.load_model(
    app.config['WIND_SPREAD_PATH'], compile=False, custom_objects=custom_objects)


classess = [
    "ants",
    "bees",
    "beetle",
    "catterpillar",
    "earthworms",
    "earwing",
    "grasshopper",
    "moth",
    "slug",
    "snail",
    "wasp",
    "weevil"
]


def image_classification(req_image):
    img = Image.open(req_image).convert("RGB")
    img = img.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x/225
    classification_result = model_classification.predict(
        x, batch_size=1)

    result = {
        "class": classess[np.argmax(classification_result)],
        "probability": str(np.max(classification_result))
    }

    return result


def wind_spread_classification(pest_name):
    result = model_wind_spread.predict(pest_name)

    return result
