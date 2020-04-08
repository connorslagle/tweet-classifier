import boto3
import botocore
import os

class BucketInterfacer():
    '''
    Class that interfaces with my local environment and S3 for my AWS account.
    Should reorg - put bucket in __init__ to call interfacer relative to selected bucket (4/7/20 9am cjs)
    set AWS creds to env variable in .bashrc for use in spark
    '''
    def __init__(self, bucket):
        self.boto3_connection = boto3.resource('s3')
        self.username = 'conslag'
        self.client = boto3.client('s3')
        self.bucket_name = self.username + bucket

    def create_bucket(self,bucket):
        self.bucket_name = self.username + bucket
        self.boto3_connection.create_bucket(Bucket=self.bucket_name)

    def send_to_bucket(self, s3_folder='', file_lst=[], path_to_dir='../data/', is_file=True):
        '''
        Method to send file (or directory of files) to s3 bucket.

        Inputs:
            - file_lst list(<str>), list of strings (even if len=0) to send to s3 bucket
            - path_to_dir <str>, relative path to local directory
            - is_file <bool>, sending single file or not
        
        Outputs: NA            
        '''
        file_lst_in_dir = os.listdir(path_to_dir)
        try:
            if is_file:
                [self.client.upload_file(f'{path_to_dir}{elem}', self.bucket_name, f'{s3_folder}{elem}') for elem in file_lst]
            else:
                [self.client.upload_file(f'{path_to_dir}{elem}', self.bucket_name, f'{s3_folder}{elem}') for elem in file_lst_in_dir]
            print(f'Successfully sent to S3 Bucket: {self.bucket_name}')

        except BaseException as e:
            print(e)
            print('An error has occured with export to S3, see BucketInterfacer class.')


    def retrieve_from_bucket(self, s3_folder='', file_lst=[], dir_dest='../data/', is_file=True):
        '''
        Method that retrieves file (or all bucket contents) from s3 bucket.

        Inputs:
            - file_lst list(<str>), list of strings (even if len=0) to retrieve from s3 bucket
            - dir_dest <str>, relative path to local directory where retrieved files will be placed
            - is_file <bool>, retrieving single file or not
        '''

        bucket_elements = [elem['Key'] for s3_file in self.client.get_paginator("list_objects_v2")\
                         .paginate(Bucket=self.bucket_name,Prefix=s3_folder) for elem in s3_file['Contents']]
        bucket_elements = bucket_elements[1:]
        print(bucket_elements)
        try:
            if is_file:
                [self.client.download_file(self.bucket_name, f'{s3_folder}{elem}', f'{dir_dest}{elem}') for elem in file_lst]
            else:
                [self.client.download_file(self.bucket_name, f'{elem}', f'{dir_dest}{elem}') for elem in bucket_elements]
            print(f'Successfully retrieved from S3 Bucket: {self.bucket_name}')

        except BaseException as e:
            print(e)
            print('An error has occured with import from S3, see BucketInterfacer class.')
    


if __name__ == "__main__":
    
    bucket = '-tweet-data-cap1'
    test_object = BucketInterfacer(bucket)

    test_object.send_to_bucket(file_lst=['del_me.txt'], path_to_dir='./', is_file=True)

    # loads all files from specified bucket
    # test_object.retrieve_from_bucket(s3_folder='test/', file_lst=['del_me.txt'])
