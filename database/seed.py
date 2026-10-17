"""
Buat akun admin dari ADMIN_* di .env

    python database/seed.py
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from app import app
from models.user_model import UserModel
from repositories.hash import hash_password

ADMIN_NAME     = os.getenv('ADMIN_NAME', 'Administrator')
ADMIN_EMAIL    = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


def seed():
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print('[error] ADMIN_EMAIL dan ADMIN_PASSWORD wajib diisi di .env')
        sys.exit(1)

    with app.app_context():
        exists = UserModel.query.execution_options(with_trashed=True).filter_by(email=ADMIN_EMAIL).first()

        if exists:
            print(f"[info] Admin {ADMIN_EMAIL} sudah ada, seed dilewati")
            return

        UserModel(
            role_id     = 1,
            name        = ADMIN_NAME,
            email       = ADMIN_EMAIL,
            password    = hash_password(ADMIN_PASSWORD),
            verified_at = datetime.now(),
        ).save()

        print(f"[ok] Admin {ADMIN_EMAIL} berhasil dibuat")


if __name__ == '__main__':
    seed()
