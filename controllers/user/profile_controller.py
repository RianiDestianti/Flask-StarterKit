from flask import g, request
from config.database import db
from models.user_model import UserModel
from repositories.hash import hash_password
from repositories.validator import Validator


class ProfileController:
    def get_profile(self):
        user = g.get('user')

        if not user:
            return {
                'status'  : 401,
                'message' : 'Token expired'
            }

        get_user = UserModel.query.filter_by(id=user['id']).first()

        return {
            'status'  : 200,
            'message' : 'Success return data user',
            'data'    : {
                **user,
                'verified'  : True if get_user and get_user.verified_at else False
            }
        }

    def action(self):
        body      = request.get_json(silent=True) or {}
        auth_user = g.get('user')

        rules = {
            'name'      : 'required',
            'password'  : 'min:6'
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        try:
            user = UserModel.query.filter_by(id=auth_user['id']).first()
            if not user:
                return {
                    'status'  : 404,
                    'message' : 'Data not found'
                }

            user.name   = body['name']
            user.phone  = body.get('phone', user.phone)
            user.avatar = body.get('avatar', user.avatar)

            if body.get('password'):
                user.password = hash_password(body['password'])

            user.save()

            return {
                'status'  : 200,
                'message' : 'Success saved data'
            }
        except Exception as error:
            db.session.rollback()
            return {
                'status'  : 500,
                'message' : str(error) or 'Failed saved data'
            }
