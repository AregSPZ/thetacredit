from dotenv import load_dotenv
import os

load_dotenv() # take environment variables from .env file

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')
    
    if not SECRET_KEY:
        raise RuntimeError("A secret key is required to use CSRF.")
