import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.tif', '.png']
    UPLOAD_PATH = os.path.join(basedir, 'app/', 'static/')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'