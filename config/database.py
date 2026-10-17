import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def database_uri():
    if os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')

    client   = os.getenv('DB_CLIENT', 'mysql+pymysql')
    host     = os.getenv('DB_HOST', '')
    port     = os.getenv('DB_PORT', '3306')
    user     = quote_plus(os.getenv('DB_USER', ''))
    password = quote_plus(os.getenv('DB_PASSWORD', ''))
    name     = os.getenv('DB_NAME', '')

    return f"{client}://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


ENGINE_OPTIONS = {
    'pool_size'     : 10,
    'max_overflow'  : 0,
    'pool_timeout'  : 30,
    'pool_recycle'  : 280,
    'pool_pre_ping' : True,
}
