import argparse
import pandas as pd
import re 
import json

def read_stop_words():
    #read from stopwords.txt
    stop_words = []
    with open('stop_words.txt', 'r') as f:
        for line in f:
            stop_words.append(line.strip())
    return stop_words

def clean_dialog(dialog):
    dialog = dialog.lower()
    dialog = re.sub(r'[()\[\],\-.?!:;#&]', ' ', dialog)
    dialog = [re.sub(r',$', '', item) for item in dialog.split()]
    dialog = [re.sub(r'[.,]{2,}', ' ', item) for item in dialog]
    
    return dialog

def compute_word_counts():
    
    topics_labelling = 'topics_label.csv'
    # Read stop words
    stop_words = read_stop_words()
    # Categories
    categories = [
    "List",
    "Ratings",
    "Announcements and Updates",
    "Ad",
    "Review",
    "Interview",
    "Rumors and Speculation"
]

    df = pd.read_csv(topics_labelling)
    # Filter rows by categories
    df_filtered = df[df['Topic'].isin(categories)]
    df_filtered['Description'] = df_filtered['Description'].apply(clean_dialog)
    # Remove stop words
    df_filtered['Description'] = df_filtered['Description'].apply(lambda x: [item for item in x if item not in stop_words])
    #make sure only alphabetic words are kept
    df_filtered['Description'] = df_filtered['Description'].apply(lambda x: [item for item in x if item.isalpha()])
    # Compute word counts
    word_counts = {}
    for topic in categories:
        word_counts[topic] = {}
        
        topic_dialog = df_filtered[df_filtered['Topic'] == topic]['Description']
        
        for dialog in topic_dialog:
            for word in dialog:
                if word not in word_counts[topic]:
                    word_counts[topic][word] = 1
                else:
                    word_counts[topic][word] += 1
   
    #keep only words that appear more than 5 times
    for topic in categories: 
       
       word_counts[topic] = {k:v for k,v in word_counts[topic].items() if v > 5}
    # Write word counts to json file
    with open('word_count.json', 'w') as f:
        json.dump(word_counts, f, indent=4)
    
    return word_counts



def main():
    parser = argparse.ArgumentParser(description='Compute word counts for each topic from all episodes of MLP.')
    #parser.add_argument('-o', dest='word_count', required=True, help='The name of the json file to output to')
   # parser.add_argument('-d', dest='clean_dialog', required=True,help='The name of the csv file to extract words from')

    args = parser.parse_args()
    #compute_word_counts()
    compute_word_counts()


if __name__ == "__main__":
    main()