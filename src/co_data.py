import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
plt.rcParams.update({'font.size': 20})

from sklearn.feature_extraction import stop_words
stopwords = stop_words.ENGLISH_STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TextCleaner():

    def __init__(self):
        self.re_substitution_groups = [r'http\S+', r'&amp; ', r"[@#]", r"[$%()*+,-./:;<=>\^_`{|}~]", r'[^a-zA-Z]']
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


def make_barchart(ax, x_label_list, y_data, y_label, title, normalize=True):
    x_vals = np.arange(len(x_label_list))
    
    if normalize:
        temp = np.array(y_data)
        temp = temp/np.sum(temp)
        y_data = list(temp)

    ax.set_position([0.13, 0.27, 0.8, 0.66])
    ax.bar(x_vals, y_data, tick_label=x_label_list, align='center', alpha=0.75)
    ax.set_ylabel(y_label)
    ax.set_ylim((0,0.20))
    ax.set_title(title)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

def make_hor_barchart(ax, set_position, x_label_list, y_data, y_label, title, normalize=True):
    x_vals = np.arange(len(x_label_list))
    
    if normalize:
        temp = np.array(y_data)
        temp = temp/np.sum(temp)
        y_data = list(temp)

    ax.set_position(set_position)
    ax.barh(x_vals, y_data, tick_label=x_label_list, align='center', alpha=0.75)
    ax.set_xlabel(y_label)
    ax.set_xlim((0,0.20))
    ax.set_title(title)
    # for label in ax.get_xticklabels():
    #     label.set_rotation(45)
    #     label.set_ha('right')

def make_hist(self, line_name, y_data, x_label, subplot_number=0, num_bins=50, normalize=True, cumulative=False):
    # x_vals = np.linspace(x_start_stop[0], x_start_stop[1], 1000)

    if self.num_subplots == 1:
        self.ax.hist(y_data, bins = num_bins, density=normalize, cumulative=cumulative, label=line_name)
        self.ax.set_ylabel('pmf' if normalize else 'count')
        # self.ax.set_ylim((0, 1) if cumulative else (0,30))
        self.ax.legend()
        self.ax.set_xlim((-0.2, 0.2))
        self.ax.set_xlabel(x_label)
    else:
        self.ax[subplot_number].hist(y_data, bins = num_bins, density=normalize, cumulative=cumulative)
        self.ax[subplot_number].set_ylabel('pmf' if normalize else 'count')
        self.ax[subplot_number].set_ylim((0, 30))
        self.ax[subplot_number].set_xlabel(x_label)


def save_fig(saved_figure_name):
    plt.savefig(f'../images/{saved_figure_name}', dpi=300)
    plt.close(fig)

def tweet_col_to_vader_df(analyzer_object, tweet_col):
    '''
    slow but works
    '''
    clean_df = pd.DataFrame()
    clean_df['tweet'] = tweet_col

    sentiment_keys = ['neg', 'pos', 'neu', 'compound']

    for key in sentiment_keys:
        clean_df[key] = [analyzer_object.polarity_scores(tweet)[key] for tweet in clean_df['tweet']]
    return clean_df
    
def bootstrap(x, resamples=1000):
    """Draw bootstrap resamples from the array x.

    Parameters
    ----------
    x: np.array, shape (n, )
      The data to draw the bootstrap samples from.
    
    resamples: int
      The number of bootstrap samples to draw from x.
    
    Returns
    -------
    bootstrap_samples: np.array, shape (resamples, n)
      The bootsrap resamples from x.
    """
    bootstrap_samples = []

    for _ in range(resamples):
        bootstrap = np.random.choice(x, size=len(x), replace=True)
        bootstrap_samples.append(bootstrap)

    return bootstrap_samples

def bootstrap_ci(sample, stat_function=np.mean, resamples=1000, ci=95):

    bootstrap_samples = bootstrap(sample,resamples=resamples)

    bootstrap_sample_means = list(map(stat_function, bootstrap_samples))

    low_bound = np.percentile(bootstrap_sample_means, (100-ci)/2)
    upper_bound = np.percentile(bootstrap_sample_means, (100+ci)/2)
    ci_bounds = [low_bound, upper_bound]

if __name__ == '__main__':
    state = 'CO'
    treatment_dict = {1: '@joebiden', 2: '@joebiden + #COVID19', 3: '#COVID19',
                      4: '@realdonaldtrump + #COVID19', 5: '@realdonaldtrump'}
    colorado_dict = {}

    for treatment in range(1,6):
        df = pd.read_csv(f'../data/{state}_{treatment}.csv', engine='python')

        raw_tweets = df['tweet_text']

        colorado_dict[treatment_dict[treatment]] = raw_tweets

    colorado_df = pd.DataFrame.from_dict(colorado_dict)

    fig, ax = plt.subplots(3,1, figsize=(10,22), sharex=True)

    fig_pos_lst = [[0.25, 0.67, 0.7, 0.30],
                  [0.25, 0.35, 0.7, 0.30],
                  [0.25, 0.03, 0.7, 0.30]]

    # ax = ax.flatten()
    for i, treatment in enumerate(['@joebiden', '#COVID19', '@realdonaldtrump']):
        total_tweet_string = colorado_df[treatment].str.cat(sep=' ')
        total_tweet_list = total_tweet_string.split()
        words, counts = to_count_list(total_tweet_list)
        if i == 2:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'Relative Frequency (a.u.)',f'Top 25 Words for {treatment}')
        else:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'',f'Top 25 Words for {treatment}')
    save_fig(f'{state}_single_word_raw_bar.png')

    fig, ax = plt.subplots(2,1, figsize=(10,22), sharex=True)

    fig_pos_lst = [[0.10, 0.51, 0.8, 0.30],
                  [0.10, 0.18, 0.8, 0.30]]

    # ax = ax.flatten()
    for i, treatment in enumerate(['@joebiden + #COVID19', '@realdonaldtrump + #COVID19']):
        total_tweet_string = colorado_df[treatment].str.cat(sep=' ')
        total_tweet_list = total_tweet_string.split()
        words, counts = to_count_list(total_tweet_list)
        if i == 1:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'Relative Frequency (a.u.)',f'Top 25 Words for {treatment}')
        else:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'',f'Top 25 Words for {treatment}')
    save_fig(f'{state}_multi_word_raw_bar.png')

    # for select_treatment in range(len(json_list)):

    #     # Clean twitter text
    #     text_cleaner = TextCleaner()
    #     clean_tweet_col = co_3_df['tweet_text'].apply(lambda x: text_cleaner.clean_tweets(x,exclude_stopwords=False))
    #     tweet_emoji = text_cleaner.emoji_list

    #     # # generate wordcloud
    #     clean_txt_string = clean_tweet_col.str.cat(sep=' ')

    #     # bar plots of freq words

    #     clean_word_list = clean_txt_string.split()

    #     keys, vals = to_count_list(clean_word_list)

        
    #     # plotter.make_barchart(0,keys[:25],vals[:25],'Relative Frequency (a.u.)',f'Top 25 Words for {treatment_dict[select_treatment]}')
    #     # plotter.save_fig(f'{select_state}_{select_treatment}_top25words.png')

    #     # VADER

    #     clean_df = tweet_col_to_vader_df(co_3_df['tweet_text'])

    #     bootstrap_samples_positive_clean = bootstrap(clean_df['pos'])

    #     bootstrap_sample_means = list(map(np.mean, bootstrap_samples_positive_clean))

    #     plotter.make_hist(f'{select_state}_{select_treatment}', bootstrap_sample_means,' Mean Positive Sentiment',normalize=False)
    # plotter.save_fig(f'{select_state}_all_mean_positive_dirty_sent.png')
    
    # emoji_df = tweet_col_to_vader_df(tweet_emoji)
    # plotter.make_hist(0,emoji_df['compound'],'Compound Sentiment',normalize=True)
    # plotter.save_fig(f'{select_state}_{select_treatment}_compound_emoji_sent.png')
