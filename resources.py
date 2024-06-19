from flask_restful import Resource
from __main__ import app
from middleware import token_required
from flask import request, jsonify
from http import HTTPStatus
from validation import PredictValidation
import uuid
import os
from dotenv import load_dotenv
from util import generate_random_list, get_desc, weather_code, save_to_gcs, allowed_files, convert_datetime_format, convert_and_add_days, get_current_time, save_to_firestore
from load_model import image_classification
from google.cloud.firestore import GeoPoint
import requests

load_dotenv()


class Predict(Resource):
    @token_required
    def post(self):
        req_image = request.files['image']
        form = PredictValidation(request.form)
        user_data = app.config['USER_DATA']
        user_id = user_data['user_id']

        if req_image and allowed_files(req_image.filename):
            if form.validate():
                current_time = get_current_time()

                filename = save_to_gcs(req_image)

                classification_result = image_classification(req_image)
                created_at = convert_datetime_format(current_time)
                delete_countdown = convert_and_add_days(current_time)
                report_id = 'report-' + str(uuid.uuid4())
                latitude = float(request.form['latitude'])
                longitude = float(request.form['longitude'])

                location = GeoPoint(latitude=latitude, longitude=longitude)

                sign = request.form['sign']
                image = f"https://storage.googleapis.com/{os.environ.get('GCP_BUCKET_NAME')}/{os.environ.get('GCP_REPORT_BUCKET_FOLDER')}/{filename}"

                description = get_desc(classification_result['class'], request.headers['Authorization'])
                
                data_input = {
                    "message": "success",
                    "data": {
                        "user_id": user_id,
                        "report_id": report_id,
                        "created_at": created_at,
                        "delete_countdown": delete_countdown,
                        "image": image,
                        "sign": sign,
                        "description": description['system'],
                        "location": location,
                        "prediction": generate_random_list(),
                        "result": classification_result
                    }
                }

                save_to_firestore(data_input)

                if float(classification_result['probability']) < 0.9:
                    result = {
                        "message": "image not classified"
                    }

                    return result

                data_return = {
                    "message": "success",
                    "data": {
                        "user_id": user_id,
                        "report_id": report_id,
                        "created_at": created_at,
                        "delete_countdown": delete_countdown,
                        "image": image,
                        "sign": sign,
                        "description": description['system'],
                        "prediction": generate_random_list(),
                        "location": {
                            "_latitude": location.latitude,
                            "_longitude": location.longitude
                        },
                        "result": classification_result
                    }
                }
                return data_return

            else:
                return jsonify({
                    'code': HTTPStatus.BAD_REQUEST,
                    'message': "all field is required"
                })
        else:
            return jsonify({
                "status": {
                    "status_code": HTTPStatus.BAD_REQUEST,
                    "message": "Invalid file format. Please upload a JPG, JPEG, or PNG image."
                }
            })


class WithoutImage(Resource):
    @token_required
    def post(self):
        form = PredictValidation(request.form)
        user_data = app.config['USER_DATA']
        user_id = user_data['user_id']
        if form.validate():
            current_time = get_current_time()
            created_at = convert_datetime_format(current_time)
            delete_countdown = convert_and_add_days(current_time)
            report_id = 'report-' + str(uuid.uuid4())

            caption = request.form['caption']
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])

            location = GeoPoint(latitude=latitude, longitude=longitude)
            sign = request.form['sign']
            image = ""
            
            description = get_desc(caption, request.headers['Authorization'])

            data_input = {
                "message": "success",
                "data": {
                    "user_id": user_id,
                    "report_id": report_id,
                    "created_at": created_at,
                    "delete_countdown": delete_countdown,
                    "location": location,
                    "image": image,
                    "sign": sign,
                    "description": description['system'],
                    "prediction": generate_random_list(),
                    "result": {
                        "class": caption,
                        "probability": ""
                    }
                }
            }

            save_to_firestore(data_input)

            data_return = {
                "message": "success",
                "data": {
                    "user_id": user_id,
                    "report_id": report_id,
                    "created_at": created_at,
                    "delete_countdown": delete_countdown,
                    "image": image,
                    "sign": sign,
                    "description": description['system'],
                    "prediction": generate_random_list(),
                    "location": {
                        "_latitude": location.latitude,
                        "_longitude": location.longitude
                    },
                    "result": {
                        "class": caption,
                        "probability": ""
                    }
                }
            }
            return data_return

        else:
            return jsonify({
                'code': HTTPStatus.BAD_REQUEST,
                'message': "all field is required"
            })


class Weather(Resource):
    @token_required
    def post(self):
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "timezone": "Asia/Bangkok",
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code"
        }

        response = requests.get(url, params=params)
        data = response.json()

        weather = weather_code(data['current']['weather_code'])

        data_return = {
            'temperature': data['current']['temperature_2m'],
            'relative_humidity': data['current']['relative_humidity_2m'],
            'feels_like': data['current']['apparent_temperature'],
            "weather": weather,
            'icon': "icon"
        }
        return data_return
