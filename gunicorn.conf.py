import os
import sys

sys.dont_write_bytecode = True

from dotenv import load_dotenv

load_dotenv()

bind    = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '3000')}"
workers = int(os.getenv('WORKERS', '4'))
timeout = 60
