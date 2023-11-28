from pathlib import Path
import pandas as pd
import json
from collect_data import KEYWORD_LIST


def get_dataset_path(fname: str) -> Path:
    return Path(__file__).parent / fname
totaldf = pd.DataFrame()
for keyword in KEYWORD_LIST:
    # Get the path for the JSON file
    json_file_path = get_dataset_path(f"filtered_news_{keyword}.json")
    with open(json_file_path, 'r', encoding='utf-8') as j:
        contents = json.load(j)
    contents = contents['articles']
    # Use list comprehension and pd.concat directly
    dataframes = [pd.DataFrame.from_records(contents[k])[['title', 'description']] for k in contents]
    emptydf = pd.concat(dataframes, ignore_index=True)
    emptydf['category'] = ''
    emptydf['keyword'] = keyword
    totaldf = pd.concat([emptydf,totaldf])
    
print('Total number of articles including duplicates '+str(len(totaldf)))
totaldf.drop_duplicates(subset=['title','description'],inplace=True)
print('Total number of articles excluding duplicates '+str(len(totaldf)))
totaldf.to_csv(f"dateframe_total.tsv",sep='\t',index_label='index', index=True, mode='w')