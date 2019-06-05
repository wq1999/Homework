import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime


def get_hot_score():
    engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
    conn = engine.connect()
    raw_data = pd.read_sql_table('post', conn)
    raw_data1 = pd.read_sql_table('comment', conn)

    post_data = raw_data[['id', 'create_time', 'read_count']]
    post_data.columns = ['post_id', 'create_time', 'read_count']
    comment_data = raw_data1[['post_id']]
    comment_data['comment_num'] = 1
    comment_data = comment_data.groupby('post_id').agg('sum').reset_index()
    post_data = pd.merge(post_data, comment_data, on='post_id', how='left')
    now = datetime.now()
    for i in post_data.index:
         days = (now - post_data.loc[i, 'create_time']).days
         hour = (now - post_data.loc[i, 'create_time']).seconds / 3600.0
         hour_gap = 24 * days + hour
         post_data.loc[i, 'hour_gap'] = hour_gap

    post_data['hot_score'] = (post_data['read_count'] * 0.1 + post_data['comment_num']) \
                             / ((post_data['hour_gap'] + 2) ** 2)
    hot_scores = post_data['hot_score'].values.tolist()
    return hot_scores
