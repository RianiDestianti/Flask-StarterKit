import sys

sys.dont_write_bytecode = True

from dotenv import load_dotenv

load_dotenv()

import os
from datetime import date, datetime
from flask import Flask, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from config.database import ENGINE_OPTIONS, database_uri, db
from routes.admin_routes import admin
from routes.user_routes import user

REQUIRED_ENV = ['DB_HOST', 'DB_USER', 'DB_NAME', 'JWT_SECRET']

missing = [key for key in REQUIRED_ENV if not os.getenv(key)]
if missing and not (os.getenv('DATABASE_URL') and os.getenv('JWT_SECRET')):
    print(f"[error] Env wajib belum diisi: {', '.join(missing)}")
    sys.exit(1)


class JSONProvider(DefaultJSONProvider):
    sort_keys = False

    @staticmethod
    def default(value):
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return DefaultJSONProvider.default(value)


app = Flask(__name__)
app.json = JSONProvider(app)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri()
if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = ENGINE_OPTIONS

db.init_app(app)

CORS(app,
    origins       = os.getenv('CORS_ORIGIN').split(',') if os.getenv('CORS_ORIGIN') else '*',
    methods       = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers = ['Content-Type', 'Authorization'],
)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user)


@app.errorhandler(HTTPException)
def http_error(error):
    message = f"Cannot {request.method} {request.path}" if error.code == 404 else error.description

    return {
        'status'  : error.code,
        'message' : message,
        'data'    : None
    }, error.code


@app.errorhandler(Exception)
def server_error(error):
    db.session.rollback()
    app.logger.exception(error)

    return {
        'status'  : 500,
        'message' : str(error) or 'Internal server error',
        'data'    : None
    }, 500


if __name__ == '__main__':
    app.run(
        host  = os.getenv('HOST', '0.0.0.0'),
        port  = int(os.getenv('PORT', '3000')),
        debug = os.getenv('APP_DEBUG', 'false').lower() == 'true',
    )
