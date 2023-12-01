import argparse
import json
from math import log

def compute_topic_lang(topics_count,num_words):

    #read json file
    with open(topics_count, 'r') as f:
        topics_count = json.load(f)
    #sort words by frequency
    topics_count = {k:sorted(v.items(), key=lambda x: x[1], reverse=True) for k,v in topics_count.items()}

    #calculate tf-idf
    topics_tfidf = {}
    for topic1 in topics_count:
        topics_tfidf[topic1] = {}
        #calculate tf-idf for each word
        for word1 in topics_count[topic1]:
            N = 1 
            #term frequency
            tf = word1[1]
            for topic2 in topics_count:
                if topic2 != topic1:
                    for word2 in topics_count[topic2]:
                        if word1[0] == word2[0]:
                            N += 1
            #inverse document frequency
            idf = log(len(topics_count) / N)
            tfidf = tf * idf
            topics_tfidf[topic1][word1[0]] = tfidf
        #sort words by tf-idf
        topics_tfidf[topic1] = sorted(topics_tfidf[topic1].items(), key=lambda x: x[1], reverse=True)
    top_n = {}
    for topic in topics_tfidf:
        for word in topics_tfidf[topic][:num_words]:
            if topic not in top_n:
                top_n[topic] = [word[0]]
            else:
                top_n[topic].append(word[0])
            json_stdout = json.dumps(top_n, indent=2)
        
    
    with open('distinctive_topic_words.json', 'w') as f:
        json.dump(top_n, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Compute topic Language')
    #parser.add_argument('-c',dest='topics_count', required=True, help='Json file')
   

    args = parser.parse_args()
    num_words=10
    topics_count = 'word_count.json'
    compute_topic_lang(topics_count,num_words)



if __name__ == '__main__':
    main()