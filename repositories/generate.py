import math
import random
from datetime import timedelta


def generate_number(length):
    characters = '1234567890'
    return ''.join(random.choice(characters) for _ in range(length))


def format_duration_smart(duration: timedelta):
    seconds = duration.total_seconds()
    days    = seconds / 86400
    hours   = seconds / 3600
    minutes = seconds / 60

    if days >= 1:
        return f"{math.floor(days)} Hari"
    elif hours >= 1:
        return f"{math.floor(hours)} Jam"
    elif minutes >= 1:
        return f"{math.floor(minutes)} Menit"
    else:
        return f"{math.floor(seconds)} Detik"


def str_words(text, words=100, end='...'):
    if not text:
        return ''

    split_text = text.strip().split()
    if len(split_text) <= words:
        return text

    return ' '.join(split_text[:words]) + end
