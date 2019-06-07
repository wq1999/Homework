import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity


def get_ratings():
    engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
    conn = engine.connect()

    user_data = pd.read_sql_table('front_user', conn)
    post_data = pd.read_sql_table('post', conn)
    comment_data = pd.read_sql_table('comment', conn)

    user_data = user_data[['id', 'username']]
    post_data = post_data[['id', 'title']]
    comment_data = comment_data[['author_id', 'post_id']]
    comment_user_id = comment_data['author_id'].values.tolist()
    comment_post_id = comment_data['post_id'].values.tolist()

    user_id = user_data['id'].values.tolist()
    user_name = user_data['username'].values.tolist()
    post_id = post_data['id'].values.tolist()
    user_map = {}
    for i in range(len(user_name)):
        user_map[user_id[i]] = user_name[i]

    ratings = {}
    for k in post_id:
        ratings[k] = {}
        for v in user_name:
            ratings[k][v] = 0

    ratings = pd.DataFrame(ratings)

    for i in range(len(comment_user_id)):
        ratings.loc[user_map[comment_user_id[i]], comment_post_id[i]] = 1
    return ratings


def predictitembased(user_name, post_id, ratings, k):
    csim_list = []
    rating = ratings.T
    for i in rating.index:
        val = cosine_similarity(rating.loc[i, :].values.reshape(1, -1),
                          rating.loc[post_id, :].values.reshape(1, -1)).item()
        csim_list.append(val)
    new_rating = pd.DataFrame({'similarity': csim_list, 'rating': rating[user_name]}, index=rating.index)
    topK = new_rating.sort_values('similarity', ascending=False)[1:(1+k)]
    topK = topK[topK['rating'] != 0]
    if len(topK) > 0:
        mean_rating = rating.loc[post_id, :].mean()
        sum = 0
        for i in topK.index:
            sum += (topK.loc[i, 'rating'] - rating.loc[i, :].mean()) * topK.loc[i, 'similarity']
        pred = (sum / topK['similarity'].sum()) + mean_rating
        # print(user_name + '->' + str(post_id) + ' rating: ' + str(pred))
    else:
        pred = 0
    return pred


def recommend_item(user_name, ratings, k):
    engine = create_engine('mysql+pymysql://root:wq19990306@localhost/demo1?charset=utf8', encoding='utf8')
    conn = engine.connect()
    post_data = pd.read_sql_table('post', conn)
    post_data = post_data[['id', 'hot_score']]
    preds = []
    post_ids = []
    for i in ratings.columns:
        if (ratings.loc[user_name, i] == 0):
            if predictitembased(user_name, i, ratings, k) != 0:
                preds.append(predictitembased(user_name, i, ratings, k))
                post_ids.append(i)
            else:
                for j in range(len(post_data)):
                    if post_data.loc[j, 'id'] == i:
                        idx = j
                        break
                preds.append(post_data.loc[idx, 'hot_score'])
                post_ids.append(i)
        else:
            pass
    recommend_list = pd.DataFrame()
    recommend_list['post_id'] = post_ids
    recommend_list['ratings'] = preds
    recommend_list = recommend_list.sort_values('ratings', ascending=False)[0:k]
    return recommend_list['post_id'].values.tolist()[0:k]
