import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


def draw_pic():
    engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
    conn = engine.connect()
    post = pd.read_sql_table('post', conn)
    comment = pd.read_sql_table('comment', conn)
    board = pd.read_sql_table('board', conn)

    post_data = post[['id', 'board_id']]
    board.columns = ['board_id', 'name', 'create_time']
    board_data = pd.merge(board, post_data, on='board_id', how='left')
    board_data = board_data[['name']]
    board_data['num'] = 1
    board_data = board_data.groupby('name').agg('sum').reset_index()
    sns.barplot(x='name', y='num', data=board_data, palette="deep")
    plt.title('板块帖子数量')
    plt.savefig('/demo/static/image/board_data.jpg')

    comment_data = comment[['post_id']]
    comment_data['comment_num'] = 1
    comment_data.groupby('post_id').agg('sum').reset_index()
    sns.barplot(x='post_id', y='comment_num', data=comment_data, palette="deep")
    plt.title('帖子评论数量')
    plt.savefig('/demo/static/image/comment_data.jpg')
