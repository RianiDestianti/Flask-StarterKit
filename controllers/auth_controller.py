from datetime import datetime
from urllib.parse import quote
from flask import request
from config.database import db
from models.user_model import UserModel
from models.verification_model import VerificationModel
from middleware.auth_middleware import sign
from repositories.generate import generate_number
from repositories.hash import compare_password, hash_password
from repositories.validator import Validator
from notifications.register_notification import registration_notification
from notifications.retry_notification import retry_notification


class AuthController:
    def login(self):
        body = request.get_json(silent=True) or {}

        rules = {
            'email'     : 'required|email',
            'password'  : 'required'
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        user = UserModel.query.filter_by(email=body['email']).first()

        if not user:
            return {
                'status'  : 401,
                'message' : 'Invalid credentials'
            }

        role = user.role.name if user.role else None

        if body.get('role') and body['role'] != role:
            return {
                'status'  : 401,
                'message' : 'Invalid credentials'
            }

        if not compare_password(body['password'], user.password):
            return {
                'status'  : 401,
                'message' : 'Invalid credentials'
            }

        token = sign({ 'email': user.email, 'role': role })
        return {
            'status'  : 200,
            'message' : 'Success logined',
            'data'    : {
                'key'     : token,
                'email'   : user.email
            }
        }

    def register(self):
        payload = request.get_json(silent=True) or {}

        rules = {
            'name'      : 'required',
            'email'     : 'required|email',
            'password'  : 'required|min:6'
        }

        validation = Validator(payload, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        check_user = UserModel.query.filter_by(email=payload['email']).first()

        if check_user:
            return {
                'status'  : 422,
                'message' : 'The email has been registered',
                'data'    : {
                    'email' : ['The email has been registered']
                }
            }

        try:
            UserModel(
                email       = payload['email'],
                name        = payload['name'],
                password    = hash_password(payload['password']),
                role_id     = 3,
                avatar      = f"https://ui-avatars.com/api/?format=png&name={quote(str(payload['name']))}"
            ).save()

            token = generate_number(6)
            VerificationModel(
                email   = payload['email'],
                value   = token
            ).save()

            registration_notification.send(payload['email'], payload['name'], token)
            register = sign({ 'email': payload['email'], 'role': 'user' })

            return {
                'status'  : 200,
                'message' : 'Successfully register',
                'data'    : {
                    'key'     : register,
                    'email'   : payload['email']
                }
            }
        except Exception as error:
            db.session.rollback()
            return {
                'status'  : 500,
                'message' : str(error) or 'Failed register',
                'data'    : None
            }

    def verify(self):
        body = request.get_json(silent=True) or {}

        rules = {
            'email'     : 'required|email',
            'code'      : 'required'
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        user = UserModel.query.filter_by(email=body['email']).first()
        if not user:
            return {
                'status'  : 422,
                'message' : 'Invalid code',
            }

        get_verification = VerificationModel.query.filter_by(email=body['email'], value=str(body['code'])).first()
        if not get_verification:
            return {
                'status'  : 422,
                'message' : 'Invalid code',
            }

        user.verified_at = datetime.now()
        user.save()

        VerificationModel.query.filter_by(email=body['email']).delete()
        db.session.commit()

        return {
            'status'  : 200,
            'message' : 'Successfully verification',
        }

    def retry_code(self):
        payload = request.get_json(silent=True) or {}

        rules = {
            'email'     : 'required|email',
        }

        validation = Validator(payload, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        user = UserModel.query.filter_by(email=payload['email']).first()

        VerificationModel.query.filter_by(email=payload['email']).delete()
        db.session.commit()

        token = generate_number(6)
        VerificationModel(
            email   = payload['email'],
            value   = token
        ).save()

        name = user.name if user else 'User'

        retry_notification.send(payload['email'], name, token)

        return {
            'status'  : 200,
            'message' : 'Successfully send code'
        }

    def reset_password(self):
        body = request.get_json(silent=True) or {}

        rules = {
            'email'     : 'required|email',
            'password'  : 'required|min:6'
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        email = str(body.get('email', '')).strip()
        user  = UserModel.query.filter_by(email=email).first()

        if not user:
            return {
                'status'  : 422,
                'message' : 'Email tidak ditemukan',
                'data'    : {
                    'email' : ['Email tidak ditemukan.']
                }
            }

        user.password = hash_password(body['password'])
        user.save()

        return {
            'status'  : 200,
            'message' : 'Password berhasil direset'
        }
