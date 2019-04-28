from apps.forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired,URL
from utils import xcache
from .models import FrontUser


class SignUpForm(BaseForm):
    username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1", message='两次输入的密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message='请输入正确格式的短信验证码！')])

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        # 因为图形验证码存储的key和值都是一样的，所以我们只要判断key是否存在就行
        if not xcache.get(graph_captcha.lower()):
            raise ValidationError(message='图形验证码错误')

    def validate_username(self, field):
        username = field.data
        user = FrontUser.query.filter_by(username=username).first()
        if user:
            raise ValidationError(message='用户名已存在')


class SignInForm(BaseForm):
    username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])


class SettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    realname = StringField()
    email = StringField()
    avatars = StringField()
    signature = StringField()
