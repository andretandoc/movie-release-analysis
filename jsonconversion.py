import pandas as pd
import json
json_file_path = "/Users/paulmandelos/Desktop/COMP370/finalproject/news_cache.json"

with open(json_file_path, 'r') as j:
     contents = json.loads(j.read())
emptydf = pd.DataFrame()     
for k in contents:
    
    lst = contents[k]
    df = pd.DataFrame.from_records(lst)
    #df['date'] = k
    df['category'] = ''
    df = df[['title','description','category']]
    emptydf = pd.concat([emptydf,df],ignore_index=True)
emptydf.to_csv('/Users/paulmandelos/Desktop/COMP370/finalproject/dataframe.tsv',sep='\t')