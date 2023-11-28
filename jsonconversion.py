from pathlib import Path
import pandas as pd
import json
from collect_data import KEYWORD_LIST


def get_dataset_path(fname: str) -> Path:
    return Path(__file__).parent / fname

totaldf = pd.DataFrame()
for keyword in KEYWORD_LIST:
    print(keyword)
    # Get the path for the JSON file
    json_file_path = get_dataset_path(f"filtered_news_{keyword}.json")
    with open(json_file_path, 'r', encoding='utf-8') as j:
        contents = json.load(j)
    contents = contents['articles']

    # Process each article
    processed_articles = []
    for date_range, articles in contents.items():
        for article in articles:
            # Extract title and description, using None if not present
            title = article.get('title')
            description = article.get('description')
            if title is not None and description is not None:
                processed_articles.append({'title': title, 'description': description})

    # Create DataFrame from processed articles
    df = pd.DataFrame(processed_articles)
    df['category'] = ''
    df['keyword'] = keyword
    totaldf = pd.concat([df, totaldf])

print('Total number of articles including duplicates ' + str(len(totaldf)))
totaldf.drop_duplicates(subset=['title', 'description'], inplace=True)
print('Total number of articles excluding duplicates ' + str(len(totaldf)))
totaldf.to_csv(f"dateframe_total.tsv", sep='\t', index_label='index', index=True, mode='w')