import os

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')
    
    if not SECRET_KEY:
        raise RuntimeError("A secret key is required to use CSRF.")
