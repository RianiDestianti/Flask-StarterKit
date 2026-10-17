from datetime import datetime
from urllib.parse import quote
from flask import request
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from config.database import db
from models.user_model import UserModel
from repositories.hash import hash_password
from repositories.validator import Validator


class UserController:
    def get_data(self):
        page    = request.args.get('page', 1, type=int)
        limit   = request.args.get('limit', 10, type=int)
        keyword = request.args.get('keyword', '')
        role    = request.args.get('role', '')

        query = UserModel.query.options(joinedload(UserModel.role)).order_by(UserModel.created_at.desc())

        if keyword:
            query = query.filter(or_(
                UserModel.name.like(f'%{keyword}%'),
                UserModel.email.like(f'%{keyword}%'),
                UserModel.phone.like(f'%{keyword}%'),
            ))

        if role:
            query = query.filter(UserModel.role_id == role)

        result = query.paginate(page=page, per_page=limit, error_out=False)

        users = [{
            'id'      : item.id,
            'name'    : item.name,
            'phone'   : item.phone,
            'email'   : item.email,
            'avatar'  : item.avatar,
            'role'    : item.role.name if item.role else None
        } for item in result.items]

        return {
            'status'  : 200,
            'message' : 'Success return data user',
            'data'    : {
                'data'      : users,
                'page'      : page,
                'limit'     : limit,
                'total'     : {
                    'pages' : result.pages,
                    'data'  : result.total
                },
            }
        }

    def action_data(self):
        body = request.get_json(silent=True) or {}
        id   = body.get('id') or 0

        rules = {
            'name'      : 'required',
            'email'     : 'required|email',
            'role'      : 'required',
            'password'  : 'min:6' if id else 'required|min:6',
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        check_email = UserModel.query.filter(UserModel.email == body['email'], UserModel.id != id).first()
        if check_email:
            return {
                'status'  : 422,
                'message' : 'The email has been registered',
                'data'    : {
                    'email' : ['The email has been registered']
                }
            }

        try:
            data = UserModel.query.filter_by(id=id).first()

            if data:

                data.name       = body['name']
                data.email      = body['email']
                data.phone      = body.get('phone')
                data.role_id    = body['role']

                if body.get('password'):
                    data.password = hash_password(body['password'])

                data.save()
            else:

                UserModel(
                    name        = body['name'],
                    email       = body['email'],
                    phone       = body.get('phone'),
                    role_id     = body['role'],
                    password    = hash_password(body['password']),
                    avatar      = f"https://ui-avatars.com/api/?format=png&name={quote(str(body['name']))}",
                    verified_at = datetime.now(),
                ).save()

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

    def get_detail(self, id):

        tmp_data = UserModel.query.options(joinedload(UserModel.role)).filter_by(id=id).first()
        if tmp_data:

            data = {
                **tmp_data.to_dict(),
                'role'      : tmp_data.role_id,
                'roleName'  : tmp_data.role.name if tmp_data.role else None,
            }

            return {
                'status'  : 200,
                'message' : 'Success return detail data',
                'data'    : data
            }
        else:
            return {
                'status'  : 404,
                'message' : 'Data not found'
            }

    def delete_data(self, id):

        data = UserModel.query.filter_by(id=id).first()
        if data:

            data.destroy()

            return {
                'status'  : 200,
                'message' : 'Success delete data'
            }
        else:
            return {
                'status'      : 404,
                'message'     : 'Data not found'
            }
