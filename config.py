import os
from dotenv import load_dotenv

load_dotenv()

class Config:
        SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv("TRACK_MODIFICATIONS"),
        DEBUG_TB_ENABLED=os.getenv("DEBUG_TB_ENABLED"),
        DEBUG_TB_INTERCEPT_REDIRECTS=os.getenv("DEBUG_TB_INTERCEPT_REDIRECTS"),
        SESSION_TYPE=os.getenv("SESSION_TYPE"),
        UPLOAD_FOLDER = '/static',
        REDIS_URL=os.getenv("REDIS_URL"),
        SECRET_KEY=os.getenv("SECRET_KEY"),
        

class ConfigDevelopment(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI")
    
    
class ConfigProduction(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_PROD_URI")
    
class ConfigTest(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_TEST_URI")
    TESTING=True