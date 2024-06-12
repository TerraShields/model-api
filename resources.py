from flask_restful import Resource
from __main__ import app
from middleware import token_required
from flask import request, jsonify
from http import HTTPStatus
from validation import PredictValidation
import uuid
import os
from dotenv import load_dotenv
from util import save_to_gcs, allowed_files, convert_datetime_format, convert_and_add_days, get_current_time, save_to_firestore
from load_model import image_classification

load_dotenv()


class GetUser(Resource):
    @token_required
    def get(self):
        user_data = app.config['USER_DATA']
        return user_data


class Predict(Resource):
    @token_required
    def post(self):
        req_image = request.files['image']
        form = PredictValidation(request.form)
        user_data = app.config['USER_DATA']
        if form.validate():
            if req_image and allowed_files(req_image.filename):
                user_id = user_data['user_id']
                current_time = get_current_time()

                filename = save_to_gcs(req_image)

                classification_result = image_classification(req_image)
                created_at = convert_datetime_format(current_time)
                delete_countdown = convert_and_add_days(current_time)
                report_id = 'report-' + str(uuid.uuid4())
                latitude = request.form['latitude']
                longitude = request.form['longitude']
                sign = request.form['sign']
                image = f"https://storage.googleapis.com/{os.environ.get('GCP_BUCKET_NAME')}/{os.environ.get('GCP_REPORT_BUCKET_FOLDER')}/{filename}"

                data_input = {
                    "message": "success",
                    "data": {
                        "user_id": user_id,
                        "report_id": report_id,
                        "created_at": created_at,
                        "delete_countdown": delete_countdown,
                        "latitude": latitude,
                        "longitude": longitude,
                        "image": image,
                        "sign": sign,
                        "description": "",
                        "result": classification_result
                    }
                }

                save_to_firestore(data_input)

                return data_input

            else:
                return jsonify({
                    "status": {
                        "status_code": HTTPStatus.BAD_REQUEST,
                        "message": "Invalid file format. Please upload a JPG, JPEG, or PNG image."
                    }
                })
        else:
            return jsonify({
                'code': HTTPStatus.BAD_REQUEST,
                'message': "all field required"
            })
