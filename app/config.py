from dotenv import load_dotenv
import os

load_dotenv() # take environment variables from .env file

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')
