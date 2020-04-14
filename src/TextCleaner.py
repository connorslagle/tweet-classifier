import re
from sklearn.feature_extraction import stop_words
stopwords = stop_words.ENGLISH_STOP_WORDS

class TextCleaner():
    '''
    This class instantiates an object with attributes of text preprocessing dictionaries and 
    a method for applying this to a list of text. 
    '''
    def __init__(self):
        self.re_substitution_groups = [r'http\S+', r'&amp; ', r"[@#]", r"[!?$%()*+,-./:;<=>\^_`{|}~]"]
        self. text_abbrevs = { 'lol': 'laughing out loud', 'bfn': 'bye for now', 'cuz': 'because',
                            'afk': 'away from keyboard', 'nvm': 'never mind', 'iirc': 'if i recall correctly',
                            'ttyl': 'talk to you later', 'imho': 'in my honest opinion', 'brb': 'be right back' }
        self.grammar_abbrevs = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                             "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                             "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                             "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                             "mustn't":"must not"}


    def clean_tweets(self, df_tweet_text, last_clean_step=5, exclude_stopwords=False):
        '''
        This function will clean the text of tweets, with ability to very the last step of cleaning.
        order:
        1. lowercase
        2. change txt abbreviations
        3. change grammar abbreviation
        4. remove punctuation
        5. remove special (utf-8) characters
        '''
        df_tweet_text = str(df_tweet_text)

        if exclude_stopwords:
            df_tweet_text_sw = ' '.join([word for word in df_tweet_text.split() if word not in stopwords])
        else:
            df_tweet_text_sw = ' '.join([word for word in df_tweet_text.split()])

        
        if last_clean_step == 0:
            clean_text = df_tweet_text_sw

        elif last_clean_step == 1:
            clean_text = df_tweet_text_sw.lower()

        elif last_clean_step == 2:
            lower = df_tweet_text_sw.lower()
            clean_text = ' '.join([self.text_abbrevs.get(elem, elem) for elem in lower.split()])
        
        elif last_clean_step == 3:
            lower = df_tweet_text_sw.lower()
            without_text_abbrevs = ' '.join([self.text_abbrevs.get(elem, elem) for elem in lower.split()])
            clean_text = ' '.join([self.grammar_abbrevs.get(elem, elem) for elem in without_text_abbrevs.split()])
        
        elif last_clean_step == 4:
            lower = df_tweet_text_sw.lower()
            without_text_abbrevs = ' '.join([self.text_abbrevs.get(elem, elem) for elem in lower.split()])
            without_grammar_abbrevs = ' '.join([self.grammar_abbrevs.get(elem, elem) for elem in without_text_abbrevs.split()])
            
            joined_re_groups = '|'.join([group for group in self.re_substitution_groups])
            clean_text = re.sub(joined_re_groups,' ',without_grammar_abbrevs)
        
        elif last_clean_step == 5:
            lower = df_tweet_text_sw.lower()
            without_text_abbrevs = ' '.join([self.text_abbrevs.get(elem, elem) for elem in lower.split()])
            without_grammar_abbrevs = ' '.join([self.grammar_abbrevs.get(elem, elem) for elem in without_text_abbrevs.split()])
            
            joined_re_groups = '|'.join([group for group in self.re_substitution_groups])
            without_re_groups = re.sub(joined_re_groups,' ',without_grammar_abbrevs)

            clean_text = re.sub(r'\W',' ',without_re_groups)
        
        words_greater_than_two_char = ' '.join([word for word in clean_text.split() if len(word) >= 2])

        one_space_separated_tweet = ' '.join([word for word in words_greater_than_two_char.split()])

        return one_space_separated_tweet