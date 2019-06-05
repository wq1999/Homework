from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BoardModel, PostModel,CommentModel


CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmission
FrontUser = front_models.FrontUser

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('用户创建成功')


@manager.command
def create_role():
    # 访问者(可以修改个人信息)
    visitor = CMSRole(name='访问者',desc='可以修改个人信息')
    visitor.permissions = CMSPermission.VISITOR

    # 运营角色(修改个人信息，管理帖子，管理评论，管理轮播图)
    operator = CMSRole(name='运营', desc='管理帖子，评论，轮播图，板块')
    operator.permissions = (CMSPermission.VISITOR|
                            CMSPermission.POSTER|
                            CMSPermission.COMMENTER|
                            CMSPermission.BOARDER)
    # 管理员(拥有绝大部分权限)
    admin = CMSRole(name='管理员', desc='管理帖子，评论，轮播图，板块，前台用户')
    admin.permissions = (CMSPermission.VISITOR|
                         CMSPermission.POSTER|
                         CMSPermission.COMMENTER|
                         CMSPermission.BOARDER|
                         CMSPermission.FRONTUSER)
    # 开发者
    developer = CMSRole(name='开发者', desc='开发人员专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_rule(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户{}添加到角色{}成功'.format(email, name))
        else:
            print('没有这个角色：{}'.format(name))
    else:
        print('没有这个用户：{}'.format(email))


@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.is_developer:
        print('用户{}有开发者的权限'.format(user.email))
    else:
        print('用户{}没有开发权限'.format(user.email))


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(username, password):
    user = FrontUser(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('成功创建前台用户：{}'.format(username))


@manager.command
def create_test_post():
    for x in range(1, 100):
        title = '标题{}'.format(x)
        content = '内容：{}'.format(x)
        board = BoardModel.query.first()
        author = FrontUser.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('测试帖子添加成功')


if __name__ == '__main__':
    manager.run()
