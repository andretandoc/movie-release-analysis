from pathlib import Path
import pandas as pd
import json

def get_dataset_path(fname: str) -> Path:
    return Path(__file__).parent / fname

# Get the path for the JSON file
json_file_path = get_dataset_path("news_cache.json")

with open(json_file_path, 'r') as j:
    contents = json.load(j)

# Use list comprehension and pd.concat directly
dataframes = [pd.DataFrame.from_records(contents[k])[['title', 'description']] for k in contents]
emptydf = pd.concat(dataframes, ignore_index=True)
emptydf['category'] = ''

# Construct the path for the TSV file in the same directory as the JSON file
tsv_file_path = get_dataset_path("dataframe.tsv")

# Save the DataFrame as TSV
emptydf.to_csv(tsv_file_path, sep='\t',index_label='index', index=True, mode='w')