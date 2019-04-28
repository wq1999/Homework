from flask import Blueprint, views, render_template, request, session
from flask import redirect, url_for
from .forms import LoginForm, ResetPwdForm, RestEmailForm
from .models import CMSUser, CMSPersmission
from .decorators import login_required, permission_required
import config
from flask import g
from exts import db
from utils import xjson
from exts import mail
from flask_mail import Message
from utils import xcache
import string
import random
from .forms import AddBannerForm, AddBoardForm,UpdateBoardForm
from apps.models import BannerModel,BoardModel
from .forms import UpdateBannerForm
from apps.models import HighlightPostModel, PostModel
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    # 当前页面
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 开始位置
    start = (page - 1) * config.PER_PAGE
    # 结束位置
    end = start + config.PER_PAGE
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page,total=total)
    posts = PostModel.query.slice(start, end)
    return render_template('cms/cms_posts.html', posts=posts, pagination=pagination)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.json_params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.json_params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return xjson.json_success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.json_params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.json_params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return xjson.json_success()


@bp.route('/dpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def dpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.json_params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.json_params_error("没有这篇帖子！")

    db.session.delete(post)
    db.session.commit()
    return xjson.json_success()


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return xjson.json_success()
    else:
        return xjson.json_params_error(message=form.get_error())


@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_params_error(message='没有这个轮播图！')
    else:
        return xjson.json_params_error(message=form.get_error())


@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return xjson.json_params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return xjson.json_params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return xjson.json_success()


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    add_form_board = AddBoardForm(request.form)
    if add_form_board.validate():
        name = add_form_board.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return xjson.json_success(message='添加板块成功')
    else:
        return xjson.json_params_error(message=add_form_board.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    update_board_form = UpdateBoardForm(request.form)
    if update_board_form.validate():
        board_id = update_board_form.board_id.data
        name = update_board_form.name.data
        if board_id:
            board = BoardModel.query.get(board_id)
            board.name = name
            db.session.commit()
            return xjson.json_success(message='更新成功')
        else:
            return xjson.json_params_error(message='板块不存在')
    else:
        return xjson.json_params_error(message=update_board_form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return xjson.json_params_error(message='请传入板块id')
    board = BoardModel.query.get(board_id)
    if not board:
        return xjson.json_params_error(message='没有这个板块')
    db.session.delete(board)
    db.session.commit()
    return xjson.json_success(message='删除板块成功')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/test_email/')
def test_email():
    msg = Message('Flask项目测试邮件',
                  recipients=['1194510922@qq.com'],
                  body='Hello, 这是一封测试邮件，这是邮件的正文')
    mail.send(msg)
    return 'success'


@bp.route('/email_captcha/')
@login_required
def email_captcha():
    # /cms/email_captcha/?email=xxxx@qq.com
    email = request.args.get('email')
    if not email:
        return xjson.json_params_error('请传递邮件参数！')

    # 生成6位数的随机验证码
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x), range(0,10)))
    captcha = ''.join(random.sample(source, 6))

    # 发送邮件
    msg = Message('BBS论坛更换邮箱验证码',
                  recipients=[email],
                  body='您的验证码：{},5分钟内有效'.format(captcha))
    try:
        mail.send(msg)
    except Exception as err:
        print(err)
        return xjson.json_server_error(message='邮件发送失败')

    # 验证码存入memcached
    xcache.set(email, captcha)
    return xjson.json_success(message='邮件发送成功')


@bp.route('/profile/')
@login_required
@permission_required(CMSPersmission.VISITOR)
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    all_boards = BoardModel.query.all()
    context = {
        'boards': all_boards
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fuser.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ADMIN)
def croles():
    return render_template('cms/cms_croles.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 如果勾选了记住我，则保存session,这样就算浏览器关闭session还是存在的
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                # return render_template('cms/cms_login.html', message='账号或密码错误')
                # 等同于以下代码
                return self.get(message='账号或密码错误')

        else:
            # login_form.errors是一个字典，如{"email":['邮箱格式错误'], "password":["密码长度为6-20位"]}
            # login_form.errors.popitem() 是取出字典的任意一项，结果是元组，如:("password":["密码长度为6-20位"])
            # 取出该元组的第2个元素：login_form.errors.popitem()[1], 如：["密码长度为6-20位"]
            # 最后取出错误提示语：login_form.errors.popitem()[1][0]
            message = login_form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        resetpwd_form = ResetPwdForm(request.form)
        if resetpwd_form.validate():
            oldpwd = resetpwd_form.oldpwd.data
            newpwd = resetpwd_form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return xjson.json_success('修改成功')
            else:
                return xjson.json_params_error('原密码错误')
        else:
            message = resetpwd_form.get_error()
            return xjson.json_params_error(message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        resetemail_form = RestEmailForm(request.form)
        if resetemail_form.validate():
            email = resetemail_form.email.data
            g.cms_user.email = email
            db.session.commit()
            return xjson.json_success('邮箱修改成功')
        else:
            message = resetemail_form.get_error()
            return xjson.json_params_error(message)


bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
