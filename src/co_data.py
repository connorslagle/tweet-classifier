import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from pipeline_to_pandas import PipelineToPandas
from s3_interfacer import BucketInterfacer

def aggregate_data_file(path_to_data_folder='../data', state='CO',treatment=0):
    '''
    This function aggregates data files imported from s3 to specific file location.
    '''
    path_to_subfolder = f'{path_to_data_folder}/{state}/{treatment}'
    new_agg_file = f'{path_to_data_folder}/{state}/{treatment}_agg.json'

    file_lst = os.listdir(path_to_subfolder)
    for elem in file_lst:
        with open(f'{path_to_subfolder}/{elem}') as f1:
            with open(new_agg_file,'a') as f2:
                lines = f1.readlines()
                for line in lines:
                    f2.write(line)

class TextCleaner():

    def __init__(self):
        self.re_substitution_groups = [r'http\S+', r'&amp; ', r"[@#]", r"[!$%()*+,-./:;<=>?\^_`{|}~]", r'[^a-zA-Z]']
        self. text_abbrevs = { 'lol': 'laughing out loud', 'bfn': 'bye for now', 'cuz': 'because',
                            'afk': 'away from keyboard', 'nvm': 'never mind', 'iirc': 'if i recall correctly',
                            'ttyl': 'talk to you later', 'imho': 'in my honest opinion', 'brb': 'be right back' }
        self.grammar_abbrevs = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                             "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                             "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                             "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                             "mustn't":"must not"}
    

    def clean_tweets(self, df_tweet_text):
        '''
        This function will clean the text of tweets:
        order:
        1. lowercase
        2. change txt abbreviations
        3. change grammar abbreviation
        4. remove non-text characters
        5. eliminate extra space
        '''
        # print(test)
        lower = df_tweet_text.lower()
        no_text_abbrevs = ' '.join([self.text_abbrevs.get(elem, elem) for elem in lower.split()])
        no_grammar_abbrevs = ' '.join([self.grammar_abbrevs.get(elem, elem) for elem in no_text_abbrevs.split()])
        
        joined_re_groups = '|'.join([group for group in self.re_substitution_groups])
        without_re_groups = re.sub(joined_re_groups,' ',no_grammar_abbrevs)
        one_space_separated_tweet = ' '.join([word for word in without_re_groups.split()])
        return one_space_separated_tweet



if __name__ == '__main__':
    '''
    # imported from s3 below:

    bucket = '-tweet-data-cap1'
    test_object = BucketInterfacer(bucket)
    test_object.retrieve_from_bucket(s3_folder='CO/', file_lst=[], dir_dest='../data/', is_file=False)

    # agged all co jsons to one below:

    co_agg_file = '../data/co_aggregate.json'
    twitter_search_term_dict = {1: ['@joebiden'], 2: ['#COVID19' '@joebiden'], 3: ['#COVID19'],
                                4: ['#COVID19' '@realdonaldtrump'], 5: ['@realdonaldtrump']}

    
    path_to_data_folder = '../data'
    state ='CO'
    for key in twitter_search_term_dict.keys():
        aggregate_data_file(state='CO', treatment=key)
    '''


    # Piped in the data to structured pd df below:

    json_list = ['1_agg.json','2_agg.json','3_agg.json','4_agg.json','5_agg.json']
    
    select_state = 'co'
    select_treatment = 4
    for i in range(len(json_list)):
        path_to_json = f'../data/CO/{json_list[i]}'
        pipeline = PipelineToPandas()
        co_3_df = pipeline.spark_df_to_pandas(path_to_json,'co',i+1)

        # Clean twitter text
        text_cleaner = TextCleaner()
        clean_tweet_col = co_3_df['tweet_text'].apply(lambda x: text_cleaner.clean_tweets(x))

        # generate wordcloud
        clean_txt_string = clean_tweet_col.str.cat(sep=' ')

        wordcloud = WordCloud().generate(clean_txt_string)
        fig, ax = plt.subplots(1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        plt.savefig(f'../images/{select_state}_{i}_cloud.png',dpi=300)

    # from sklearn.feature_extraction.text import CountVectorizer

    # tfidf