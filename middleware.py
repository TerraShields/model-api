import jwt
from __main__ import app, db
from flask import request, jsonify
from http import HTTPStatus
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.split(' ')[1]
        if not token:
            return jsonify({
                "message": "Unauthorized",
                "status_code": HTTPStatus.UNAUTHORIZED
            })
        try:
            token = jwt.decode(
                token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user_id = token['user_id']

            users_query = db.collection(u'users').where(
                u'user_id', u'==', user_id)
            for doc in users_query.stream():
                user_data = doc.to_dict()
            app.config['USER_DATA'] = user_data
        except:
            return jsonify({
                'errors': 'Unauthorized',
                "status_code": HTTPStatus.UNAUTHORIZED
            })
        return f(*args, **kwargs)
    return decorator
