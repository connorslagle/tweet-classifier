import pandas as pd
import numpy as np
import os
import re
import plotting_functions
import TextCleaner



from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer





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




def tweet_col_to_vader_df(analyzer_object, tweet_col):
    '''
    slow but works
    '''
    vader_df = pd.DataFrame()
    vader_df['tweet'] = tweet_col

    sentiment_keys = ['neg', 'pos', 'neu', 'compound']

    for key in sentiment_keys:
        vader_df[key] = [analyzer_object.polarity_scores(str(tweet))[key] for tweet in vader_df['tweet']]
    return vader_df
    
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

def make_sent_sensitivity_array (text_df, treatment, sentiment_type, num_resamples, total_cleaning_steps_list=range(1,6)):
    '''
    Performs iterative tweet pre-processing, scores with VADER algorithm and computed the bootstrapped sample means.
    '''
    sample_means_array = np.zeros((num_resamples, len(total_cleaning_steps_list)))

    for step in total_cleaning_steps_list:
        clean_tweet_col = text_df[treatment].apply(lambda x: cleaner.clean_tweets(x,last_clean_step=step))
        vader_df = tweet_col_to_vader_df(analyzer, clean_tweet_col)

        bootstrap_samples = bootstrap(vader_df[sentiment_type],resamples=1000)
        bootstrap_sample_means = list(map(np.mean, bootstrap_samples))

        sample_means_array[:,step-1] = bootstrap_sample_means
    return sample_means_array

if __name__ == '__main__':
    '''
    Imports all csv files for given state for analysis.
    '''
    state = 'CO'
    treatment_dict = {1: '@joebiden', 2: '@joebiden + #COVID19', 3: '#COVID19',
                      4: '@realdonaldtrump + #COVID19', 5: '@realdonaldtrump'}
    colorado_dict = {}

    for treatment in range(1,6):
        df = pd.read_csv(f'../data/{state}_{treatment}.csv', engine='python')

        raw_tweets = df['tweet_text']

        colorado_dict[treatment_dict[treatment]] = raw_tweets

    colorado_df = pd.DataFrame.from_dict(colorado_dict)

    '''
    Plotting fig 1: Raw (unprocessed tweets)
    '''
    fig, ax = plt.subplots(3,1, figsize=(10,22), sharex=True)

    fig_pos_lst = [[0.25, 0.67, 0.7, 0.30],
                  [0.25, 0.35, 0.7, 0.30],
                  [0.25, 0.03, 0.7, 0.30]]


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


    for i, treatment in enumerate(['@joebiden + #COVID19', '@realdonaldtrump + #COVID19']):
        total_tweet_string = colorado_df[treatment].str.cat(sep=' ')
        total_tweet_list = total_tweet_string.split()
        words, counts = to_count_list(total_tweet_list)
        if i == 1:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'Relative Frequency (a.u.)',f'Top 25 Words for {treatment}')
        else:
            make_hor_barchart(ax[i],fig_pos_lst[i],words[:25][::-1],counts[:25][::-1],'',f'Top 25 Words for {treatment}')
    save_fig(f'{state}_multi_word_raw_bar.png')

    '''
    VADER analysis on RAW tweets
    '''
    analyzer = SentimentIntensityAnalyzer()

    for i, treatment in enumerate(treatment_dict.values()):
        fig, ax = plt.subplots(1,figsize=(8,6))
        vader_df = tweet_col_to_vader_df(analyzer, colorado_df[treatment])
        make_hist(ax, treatment, vader_df['compound'], (0,4000), 'Compound Sentiment', (-1, 1))
        save_fig(f'{state}_{i}_raw_compound_sentiment.png')

    '''
    Bootstrap raw tweets
    '''

    fig, ax = plt.subplots(1,figsize=(8,6))
    for i, treatment in enumerate(treatment_dict.values()):

        vader_df = tweet_col_to_vader_df(analyzer, colorado_df[treatment])

        bootstrap_samples = bootstrap(vader_df['compound'],resamples=1000)
        bootstrap_sample_means = list(map(np.mean, bootstrap_samples))

        make_hist(ax, treatment, bootstrap_sample_means, (0,120), 'Mean Compound Sentiment', (-1, 1))
    save_fig(f'{state}_all_raw__mean_compound_sentiment.png')

    '''
    preprocess tweets, perform VADER analysis, and make sensitivity boxplots
    '''
    cleaner = TextCleaner()
    num_resamples = 1000
    total_cleaning_steps = range(1,6)

    

    for i, treatment in enumerate(treatment_dict.values()):
        two_dim_array = make_sent_sensitivity_array(colorado_df, treatment, 'compound', num_resamples, total_cleaning_steps)

        # make boxplots
        fig, ax = plt.subplots(1,figsize=(8,6))
        make_boxplot(ax,two_dim_array,(0,0.15),total_cleaning_steps,'Mean Negative Sentiment',title=f'Text Cleaning Sensitivity for\n{treatment}')
        save_fig(f'{state}_{i}_mean_negative_boxplot.png')