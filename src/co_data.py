import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import stop_words
stopwords = stop_words.ENGLISH_STOP_WORDS
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


    def clean_tweets(self, df_tweet_text, exclude_stopwords=False):
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
        
        joined_re_groups = '|'.join([group for group in self.re_substitution_groups[:3]])
        without_re_groups = re.sub(joined_re_groups,' ',no_grammar_abbrevs)
        
        self.emoji_list = re.sub(r'\w','',without_re_groups).split()     # encode with utf-8

        without_last_re_group = re.sub(self.re_substitution_groups[4],' ', without_re_groups)
        words_greater_than_two_char = ' '.join([word for word in without_last_re_group.split() if len(word) >= 2])

        if exclude_stopwords:
            one_space_separated_tweet = ' '.join([word for word in words_greater_than_two_char.split() if word not in stopwords])
        else:
            one_space_separated_tweet = ' '.join([word for word in words_greater_than_two_char.split()])
        return one_space_separated_tweet

def make_cloud(ax, pd_series_cleaned_text, state='CO', treatment='2', save_fig = False):
    clean_txt_string = pd_series_cleaned_text.str.cat(sep=' ')

    wordcloud = WordCloud().generate(clean_txt_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    plt.savefig(f'../images/{state}_{treatment}_cloud.png',dpi=300)

def to_count_list(input_lst, sorted_by_vals_desc=True):
    '''
    Counts words in word list, converts to count dictionary, then outputs
    words (keys) and counts (vals)
    '''
    new_dict ={}
    for word in input_lst:
        if word not in new_dict:
            new_dict[word] = 1
        else:
            new_dict[word] += 1
    
    if sorted_by_vals_desc:
        keys = sorted(new_dict, key=new_dict.__getitem__, reverse=True)
        values = [new_dict[elem] for elem in keys]
    else:
        keys = list(new_dict.keys())
        values = list(new_dict.values())

    return keys, values

class PlotFormatter():
    '''
    Formats and plots different plots (bar chart, sentiment pdfs)
    '''
    def __init__(self, subplots=1, figsize=(12,8), style='ggplot'):
        self.fig, self.ax = plt.subplots(subplots,figsize=figsize)
        self.num_subplots = subplots
        plt.style.use(style)
        plt.rcParams.update({'font.size': 18})

    def barchart(self, subplot_number, x_label_list, y_data, y_label, title, normalize=True):
        x_vals = np.arange(len(x_label_list))
        
        if normalize:
            temp = np.array(y_data)
            temp = temp/np.sum(temp)
            y_data = list(temp)

        if self.num_subplots == 1:
            self.ax.set_position([0.15, 0.25, 0.8, 0.6])
            self.ax.bar(x_vals, y_data, tick_label=x_label_list, align='center', alpha=0.75)
            self.ax.set_ylabel(y_label)
            self.ax.set_ylim((0,0.40))
            self.ax.set_title(title)
            for label in self.ax.get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')
        else:
            self.ax[subplot_number].bar(x_vals, y_data, tick_label=x_label_list, align='center', alpha=0.75)
            self.ax[subplot_number].set_ylabel(y_label)
            self.ax.set_ylim((0,0.40))
            self.ax[subplot_number].set_title(title)
            for label in self.ax[subplot_number].get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

    def save_fig(self,saved_figure_name):
        plt.savefig(f'../images/{saved_figure_name}', dpi=300)
        plt.close(self.fig)


    

if __name__ == '__main__':
    '''
    # imported from s3 below:

    bucket = '-tweet-data-cap1'
    test_object = BucketInterfacer(bucket)
    test_object.retrieve_from_bucket(s3_folder='CO/', file_lst=[], dir_dest='../data/', is_file=False)

    # agged all co jsons to one below:

    co_agg_file = '../data/co_aggregate.json'
    twitter_search_term_dict = {1: ['@joebiden'], 2: ['#COVID19' '@joebiden'], 3: ['#COVID19'],
                                4: ['#COVID19' '@   realdonaldtrump'], 5: ['@realdonaldtrump']}

    
    path_to_data_folder = '../data'
    state ='CO'
    for key in twitter_search_term_dict.keys():
        aggregate_data_file(state='CO', treatment=key)
    '''


    # Piped in the data to structured pd df below:

    json_list = ['1_agg.json','2_agg.json','3_agg.json','4_agg.json','5_agg.json']
    
    select_state = 'co'
    select_treatment = 2

    treatment_dict = {0: '@joebiden', 1: '@joebiden & #covid19', 2: '#covid19',
                      3: '@realdonaldtrump & #covid19', 4: '@realdonaldtrump'}

    for select_treatment in range(len(json_list)):
        path_to_json = f'../data/CO/{json_list[select_treatment]}'
        pipeline = PipelineToPandas()
        co_3_df = pipeline.spark_df_to_pandas(path_to_json,select_state,select_treatment+1)

        # Clean twitter text
        text_cleaner = TextCleaner()
        clean_tweet_col = co_3_df['tweet_text'].apply(lambda x: text_cleaner.clean_tweets(x,exclude_stopwords=True))
        tweet_emoji = text_cleaner.emoji_list

        # # generate wordcloud
        clean_txt_string = clean_tweet_col.str.cat(sep=' ')

        # bar plots of freq words

        clean_word_list = clean_txt_string.split()

        keys, vals = to_count_list(clean_word_list)

        plotter = PlotFormatter()
        plotter.barchart(0,keys[:25],vals[:25],'word relative frequency (a.u.)',f'Top 25 words for {treatment_dict[select_treatment]}, w/o stopwords')
        plotter.save_fig(f'{select_state}_{select_treatment}_top25words_nostops.png')

    # from sklearn.feature_extraction.text import CountVectorizer

    # tfidf