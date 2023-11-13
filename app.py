import numpy as np
from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the sign language alphabet prediction model
sign_language_model = load_model("asl_vgg16_best_weights.h5", compile=False)
sign_language_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((64, 64))
    img = np.array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    sign_language_prediction = None
    image_path = None

    if request.method == 'POST' and 'image' in request.files:
        try:
            f = request.files['image']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath, 'uploads', f.filename)
            f.save(filepath)

            img = preprocess_image(filepath)
            predictions = sign_language_model.predict(np.array([img]))

            if len(predictions) > 0:
                max_prediction_index = np.argmax(predictions)
                if 0 <= max_prediction_index < len(sign_language_labels):
                    sign_language_prediction = sign_language_labels[max_prediction_index]
                else:
                    sign_language_prediction = "Nothing or Space"
            else:
                sign_language_prediction = "No Predictions Available"

            image_path = '/uploads/' + f.filename  # Adjust the path as needed
        except Exception as e:
            print("An error occurred:", str(e))

    return render_template('predict.html', pred=sign_language_prediction, image_path=image_path)


if __name__ == "__main__":
    app.run(debug=True)
