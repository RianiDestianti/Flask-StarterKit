import bcrypt


def hash_password(password, rounds=10):
    return bcrypt.hashpw(str(password).encode(), bcrypt.gensalt(rounds)).decode()


def compare_password(password, hashed):
    try:
        return bcrypt.checkpw(str(password).encode(), str(hashed).encode())
    except ValueError:
        return False
