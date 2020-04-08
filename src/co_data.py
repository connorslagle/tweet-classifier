import pandas as pd
import numpy as np
import sklearn as skl
import os
from pipeline_to_pandas import PipelineToPandas
from s3_interfacer import BucketInterfacer

def aggregate_data_file(path_to_data_folder, new_file_name, state='CO',treatment=0):
    path_to_subfolder = f'{path_to_data_folder}/{state}/{treatment}'
    file_lst = os.listdir(path_to_subfolder)
    
    for elem in file_lst:
        with open(f'{path_to_subfolder}/{elem}') as f1:
            with open(new_file_name,'a') as f2:
                lines = f1.readlines()
                for line in lines:
                    f2.write(line)

if __name__ == '__main__':
    # imported from s3 below:

    # bucket = '-tweet-data-cap1'
    # test_object = BucketInterfacer(bucket)
    # test_object.retrieve_from_bucket(s3_folder='CO/', file_lst=[], dir_dest='../data/', is_file=False)

    # agged all co jsons to one bwloe:

    co_agg_file = '../data/co_aggregate.json'
    # aggregate_data_file('../data/CO/', co_agg_file)

    twitter_search_term_dict = {1: ['@joebiden'], 2: ['#COVID19' '@joebiden'], 3: ['#COVID19'],
                                4: ['#COVID19' '@realdonaldtrump'], 5: ['@realdonaldtrump']}
    
    # Piped in the data to structured pd df below:

    # pipeline = PipelineToPandas()
    # pipeline.load_to_spark_df(co_agg_file)
    # pipeline.truncate_spark_df('co', 5)
    # tweet_df = pipeline.spark_df_to_pandas()

    # from sklearn.feature_extraction.text import CountVectorizer
