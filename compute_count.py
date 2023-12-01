import argparse
import pandas as pd
import re
import json

STOP_WORDS_FILE = 'stop_words.txt'
TOPICS_LABEL_FILE = 'topics_label.csv'
OUTPUT_FILE = 'word_count.json'
MIN_WORD_FREQUENCY = 5

def read_stop_words(stop_words_file):
    stop_words = []
    with open(stop_words_file, 'r') as f:
        for line in f:
            stop_words.append(line.strip())
    return stop_words

def clean_description(description):
    description = description.lower()
    description = re.sub(r'[()\[\],\-.?!:;#&]', ' ', description)
    description = [re.sub(r',$', '', item) for item in description.split()]
    description = [re.sub(r'[.,]{2,}', ' ', item) for item in description]
    return description

def filter_and_preprocess(df, categories, stop_words):
    df_filtered = df[df['Topic'].isin(categories)]
    df_filtered['Description'] = df_filtered['Description'].apply(clean_description)
    df_filtered['Description'] = df_filtered['Description'].apply(lambda x: [item for item in x if item not in stop_words])
    df_filtered['Description'] = df_filtered['Description'].apply(lambda x: [item for item in x if item.isalpha()])
    return df_filtered

def compute_word_counts(df_filtered, categories, min_word_frequency):
    word_counts = {}
    for topic in categories:
        word_counts[topic] = {}
        topic_description = df_filtered[df_filtered['Topic'] == topic]['Description']
        for description in topic_description:
            for word in description:
                word_counts[topic][word] = word_counts[topic].get(word, 0) + 1

    # Keep only words that appear more than MIN_WORD_FREQUENCY times
    for topic in categories:
        word_counts[topic] = {k: v for k, v in word_counts[topic].items() if v > min_word_frequency}

    # Write word counts to json file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(word_counts, f, indent=4)

    return word_counts

def main():
    parser = argparse.ArgumentParser(description='Compute word counts for each topic from all episodes of MLP.')
    args = parser.parse_args()

    stop_words = read_stop_words(STOP_WORDS_FILE)
    df = pd.read_csv(TOPICS_LABEL_FILE)
    categories = ["List", "Ratings", "Announcements and Updates", "Ad", "Review", "Interview", "Rumors and Speculation"]

    df_filtered = filter_and_preprocess(df, categories, stop_words)
    compute_word_counts(df_filtered, categories, MIN_WORD_FREQUENCY)

if __name__ == "__main__":
    main()
