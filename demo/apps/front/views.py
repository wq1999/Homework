from flask import Blueprint,views,render_template,request,session,g,redirect,url_for
from .forms import SignUpForm
from utils import xjson
from .models import FrontUser
from exts import db
from utils import safeutils
import config
from .forms import SignInForm,AddPostForm,SettingsForm
from apps.models import BannerModel,BoardModel,PostModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from flask import abort
from .forms import AddCommentForm
from apps.models import CommentModel
from apps.models import HighlightPostModel
from sqlalchemy.sql import func

bp = Blueprint('front', __name__)


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    if not post.read_count:
        post.read_count = 1
    else:
        post.read_count += 1
    db.session.commit()
    return render_template('front/front_pdetail.html', post=post)


@bp.route('/search/')
def search():
    q = request.args.get('query')
    return q


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    boards = BoardModel.query.all()

    # 当前页面
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 开始位置
    start = (page - 1) * config.PER_PAGE
    # 结束位置
    end = start + config.PER_PAGE

    board_id = request.args.get('bd',type=int, default=None)
    sort = request.args.get("st", type=int, default=1)
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序,点赞功能没有做，所以这里用时间倒序排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()

    pagination = Pagination(bs_version=4,page=page, total=total)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)


@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.signin'))


@bp.route('/settings/',methods=['POST','GET'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingsForm(request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            email = form.email.data
            avatar = form.avatars.data
            signature = form.signature.data

            user_model = g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            if email:
                user_model.email = email
            if avatar:
                user_model.avatars = avatar
            if signature:
                user_model.signature = signature
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_params_error(message=form.get_error())


@bp.route('/profile/<user_id>',methods=['GET'])
@login_required
def profile(user_id=0):
    if not user_id:
        return abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return render_template('front/front_profile.html',**context)
    else:
        return abort(404)


@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    add_comment_form = AddCommentForm(request.form)
    if add_comment_form.validate():
        content = add_comment_form.content.data
        post_id = add_comment_form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_params_error('没有这篇帖子！')
    else:
        return xjson.json_params_error(add_comment_form.get_error())


@bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        add_post_form = AddPostForm(request.form)
        if add_post_form.validate():
            title = add_post_form.title.data
            content = add_post_form.content.data
            board_id = add_post_form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return xjson.json_params_error(message='没有这个板块')
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_params_error(message=add_post_form.get_error())


class SignUpViews(views.MethodView):
    def get(self):
        # 获取上一个页面的url
        return_to = request.referrer
        # referrer不一定会存在，比如直接访问的登录页面
        # 并且它不等于登录页面的url
        # 并且这个referre是个安全的url,防止恶意者去伪造它，被跳转到其它恶意的网站
        if return_to and return_to !=request.url and safeutils.is_safe_url(return_to):
            # 把这个url传入到模板中
            return render_template('front/front_signup.html', return_to=return_to)
        return render_template('front/front_signup.html')

    def post(self):
        signup_form = SignUpForm(request.form)
        if signup_form.validate():
            username = signup_form.username.data
            password = signup_form.password1.data
            user = FrontUser(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return xjson.json_success('恭喜您，注册成功')
        else:
            return xjson.json_params_error(signup_form.get_error())


class SignInViews(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        return render_template('front/front_signin.html')

    def post(self):
        signin_form = SignInForm(request.form)
        if signin_form.validate():
            username = signin_form.username.data
            password = signin_form.password.data
            remember = signin_form.remember.data
            user = FrontUser.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return xjson.json_success('登录成功')
            else:
                return xjson.json_params_error('用户名或密码错误')
        else:
            return xjson.json_params_error(signin_form.get_error())


bp.add_url_rule('/signup/', view_func=SignUpViews.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignInViews.as_view('signin'))
