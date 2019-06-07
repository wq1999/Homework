import pandas as pd
from sqlalchemy import create_engine
import re


def clean(content):
    reg = re.compile('<[^>]*>')
    content = reg.sub('', content).replace('\n', '')
    return content


engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
conn = engine.connect()
comment_data = pd.read_sql_table('comment', conn)
comments = comment_data[['content']]
for i in comments.index:
    comments.loc[i, 'content'] = clean(comments.loc[i, 'content'])

print(comments)
text = comments.values.tolist()[1]
