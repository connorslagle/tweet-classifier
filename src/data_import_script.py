from pipeline_to_pandas import PipelineToPandas
from s3_interfacer import BucketInterfacer
import os

'''
This will grab data from s3 -> spark -> local csv
'''

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


if __name__ == "__main__":
    state_list = ['AR','OR']
    bucket = '-tweet-data-cap1'
    test_object = BucketInterfacer(bucket)
    for state in state_list:
        test_object.retrieve_from_bucket(s3_folder=f'{state}/', file_lst=[], dir_dest=f'../data/', is_file=False)

    # for state in state_list:
    #     path_to_json = f'../data/{state}/{json_list[select_treatment]}'
    
    # co_3_df = pipeline.spark_df_to_pandas(path_to_json,select_state,select_treatment+1)
        
    #     path_to_data_folder = '../data'
    #     state ='CO'
    #     for key in twitter_search_term_dict.keys():
    #         aggregate_data_file(state='CO', treatment=key)


    #     # Piped in the data to structured pd df below:

    #     json_list = ['1_agg.json','2_agg.json','3_agg.json','4_agg.json','5_agg.json']
        
    #     select_state = 'co'
    #     select_treatment = 0

    #     treatment_dict = {0: '@joebiden', 1: '@joebiden & #covid19', 2: '#covid19',
    #                     3: '@realdonaldtrump & #covid19', 4: '@realdonaldtrump'}

    #     pipeline = PipelineToPandas()

