import re
from datetime import datetime, timedelta, timezone
import pytz
from __main__ import app, db
import os
import uuid
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

client = storage.Client(project=os.environ.get("GCP_PROJECT_ID"))
bucket_name = os.environ.get("GCP_BUCKET_NAME")
bucket = storage.Bucket(client, bucket_name)


def allowed_files(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXT']


def generate_filename(original_filename):
    base, ext = os.path.splitext(original_filename)
    new_filename = str(uuid.uuid4()) + ext
    sanitized_filename = os.path.sep.join([os.path.dirname(
        original_filename), os.path.basename(os.path.splitext(new_filename)[0]) + ext])
    sanitized_filename = re.sub(r"\\", "", sanitized_filename)

    return sanitized_filename


def get_current_time():
    current_time = datetime.now(
        timezone.utc)
    adjusted_time = current_time + timedelta(hours=7)
    return adjusted_time.isoformat()


def convert_datetime_format(input_datetime_str, desired_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    input_datetime = datetime.strptime(
        input_datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    input_datetime = input_datetime.astimezone(pytz.utc)
    output_datetime_str = input_datetime.strftime(desired_format)
    return output_datetime_str


def convert_and_add_days(input_datetime_str, desired_format="%Y-%m-%dT%H:%M:%S.%fZ", days_to_add=7):
    input_datetime = datetime.strptime(
        input_datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    input_datetime = input_datetime.astimezone(pytz.utc)

    if len(re.findall(r"\.\d{3}", input_datetime_str)) > 0:
        output_datetime_str = input_datetime.strftime(desired_format)
        output_datetime_str = re.sub(r"\.\d{3}", ".000", output_datetime_str)
    else:
        output_datetime_str = input_datetime.strftime(desired_format)

    time_delta = timedelta(days=days_to_add)
    adjusted_datetime = input_datetime + time_delta

    return adjusted_datetime.strftime(desired_format)


def save_to_gcs(req_image):
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filename = generate_filename(req_image.filename)
    filepath = os.path.join(upload_folder, filename)
    req_image.save(filepath)

    blob = bucket.blob('reports/' + filename)
    blob.upload_from_filename(filepath)

    os.remove(filepath)

    return filename


def save_to_firestore(data):
    data_input = data['data']
    collection = db.collection(f"reports")
    collection_doc = collection.document(f"{data_input['report_id']}")
    collection_doc.set({
        'created_at': data_input['created_at'],
        'delete_countdown': data_input['delete_countdown'],
        'description': data_input['description'],
        'image': data_input['image'],
        'latitude': data_input['latitude'],
        'longitude': data_input['longitude'],
        'user_id': data_input['user_id'],
        'report_id': data_input['report_id'],
        'sign': data_input['sign'],
        'classification_result': data_input['result']['class'],
    })

    return data_input
