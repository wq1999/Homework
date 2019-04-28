from flask import Blueprint, make_response
from utils.captcha import Captcha
from io import BytesIO
from utils import xcache
from flask import jsonify
import qiniu

bp = Blueprint('common', __name__, url_prefix='/c')


@bp.route('/')
def index():
    return 'common index'


@bp.route('/graph_captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    xcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = 'Y9ePn56AAscdcibCD4bzGzbIu07pcDEiQt_zUwHN'
    secret_key = 'ur1iSKXt8Ad3L9olAsd3XJZcavzVjdcLyV120TzX'
    q = qiniu.Auth(access_key, secret_key)

    bucket = 'demo'
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})
