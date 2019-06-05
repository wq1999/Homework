import pandas as pd
from sqlalchemy import create_engine
import re
from utils.postRecommend import get_ratings, recommend_item

engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
conn = engine.connect()
raw_data = pd.read_sql_table('post', conn)


def clean(data):
    for i in range(len(data)):
        content = data['content'][i]
        reg = re.compile('<[^>]*>')
        content = reg.sub('', content).replace('\n', '')
        data['content'][i] = content
    return data


process_data = clean(raw_data)
contents = process_data['content'].values.tolist()
print(contents)
