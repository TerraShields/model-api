from flask import Flask
from flask_restful import Api
from google.cloud import firestore
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

db = firestore.Client(project=os.environ.get("GCP_PROJECT_ID"))

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config["JWT_ALGORITHM"] = "HS256"

app.config["UPLOAD_FOLDER"] = "upload/"
app.config['ALLOWED_EXT'] = set(['png', 'jpg', 'jpeg'])
app.config['MODEL_PATH'] = "./models/pest_label_classifier.h5"
app.config['WIND_SPREAD_PATH'] = "./models/wind_spread_classifier_model.h5"

import resources

api.add_resource(resources.Predict, '/api/report')
api.add_resource(resources.WithoutImage, '/api/report/capt')
# api.add_resource(resources.ChatBot, '/api/chat')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 8080))
