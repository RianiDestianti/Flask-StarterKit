import os
import re
from datetime import datetime, timedelta, timezone
import jwt
from flask import g, request
from models.user_model import UserModel

JWT_SECRET     = os.getenv('JWT_SECRET', '')
JWT_EXPIRES_IN = os.getenv('JWT_EXPIRES_IN', '1y')

UNITS = { 's': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31557600 }


def sign(payload):
    match   = re.fullmatch(r'(\d+)\s*([smhdwy]?)', JWT_EXPIRES_IN.strip())
    seconds = int(match.group(1)) * UNITS.get(match.group(2) or 's', 1) if match else UNITS['y']
    now     = datetime.now(timezone.utc)

    return jwt.encode({ **payload, 'iat': now, 'exp': now + timedelta(seconds=seconds) }, JWT_SECRET, algorithm='HS256')


def auth_middleware(next):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return { 'status': 401, 'message': 'Unauthorized', 'data': None }, 401

    token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else ''

    if not token or not JWT_SECRET:
        return { 'status': 401, 'message': 'Missing token or JWT secret', 'data': None }, 401

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user    = UserModel.query.filter_by(email=decoded.get('email')).first()

        if not user:
            raise ValueError('User not found')

        g.user  = {
            'id'      : user.id,
            'name'    : user.name,
            'email'   : user.email,
            'role'    : user.role.name if user.role else None,
            'avatar'  : user.avatar,
        }
    except Exception:
        return { 'status': 403, 'message': 'Invalid or expired token', 'data': None }, 403

    return next()


def admin_only(next):
    user = g.get('user')

    if not user or user['role'] != 'admin':
        return { 'status': 403, 'message': 'Forbidden: Admins only', 'data': None }, 403

    return next()


def tutorn_admin(next):
    user = g.get('user')

    if not user or user['role'] != 'admin' and user['role'] != 'tutor':
        return { 'status': 403, 'message': 'Forbidden: Admins and Tutor only', 'data': None }, 403

    return next()
