from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length
from apps.forms import BaseForm
from wtforms.validators import Length, EqualTo
from wtforms.validators import ValidationError
from .models import CMSUser
from utils import xcache


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,30, message='密码长度6-30')])
    newpwd = StringField(validators=[Length(6,30, message='密码长度6-30')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='新密码输入不一致')])


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20, message='密码长度为6-20位')])
    remember = IntegerField()


class RestEmailForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误'),InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='验证码长度错误')])

    def validate_email(self, field):
        user = CMSUser.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('该邮箱已存在')

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xcache.get(email)
        # 判断memcached中是否有对应的邮箱及验证码，小写进行比较，这样用户可以不区分大小写
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
