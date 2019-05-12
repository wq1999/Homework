import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1')
conn = engine.connect()
data = pd.read_sql_table('comment', conn)
print(data['content'])
