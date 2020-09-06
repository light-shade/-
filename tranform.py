import pandas as pd
df = pd.read_csv('data.csv')
ids = df['id'].values.tolist()
fieldnames = [
    'id',
    'tit',
    'star',
    'comments',
    'avg_price',
    'cate',
    'tag',
    'region',
    'address',
    'tasty_score',
    'env_score',
    'ser_score',
]
df.drop_duplicates(subset=['id'], keep='first', inplace=True)
df.to_excel('data.xlsx', index=False, header=fieldnames)