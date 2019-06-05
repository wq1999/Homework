import os
from datetime import timedelta

# session
SECRET_KEY = os.urandom(24)
# 设置session有效期为2天，若开启了session.permanent后不设置该参数，则默认为31天
PERMANENT_SESSION_LIFETIME = timedelta(days=31)

DEBUG = True
CMS_USER_ID = 'HEBOANHEHE'
FRONT_USER_ID = 'WFQQ132FEVFW'

# MySQL Database
HOST = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'wq19990306'
DATABASE = 'demo1'

DB_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset-utf8'.format(username=USERNAME,
                                                                                        password=PASSWORD,
                                                                                        host=HOST,
                                                                                        port=PORT,
                                                                                        db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True
MAIL_USERNAME = '17784452018@163.com'
MAIL_PASSWORD = 'wq1194510922'   # 注意，这里的密码不是邮箱密码，而是授权码
MAIL_DEFAULT_SENDER = '17784452018@163.com'

# 上传到本地
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'images')

# 上传到七牛
UEDITOR_UPLOAD_TO_QINIU = True  # 如果上传到七牛这里设置为True，上传到本地则为False
UEDITOR_QINIU_ACCESS_KEY = "Y9ePn56AAscdcibCD4bzGzbIu07pcDEiQt_zUwHN"
UEDITOR_QINIU_SECRET_KEY = "ur1iSKXt8Ad3L9olAsd3XJZcavzVjdcLyV120TzX"
UEDITOR_QINIU_BUCKET_NAME = "demo"
UEDITOR_QINIU_DOMAIN = 'http://prlevuauy.bkt.clouddn.com/'

# 每页显示10篇帖子
PER_PAGE = 10
