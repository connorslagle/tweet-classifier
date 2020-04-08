import boto3
import os

boto3_connection = boto3.resource('s3')

username = os.environ['USER']
bucket_name = username + "-tweet-data-cap1"
boto3_connection.create_bucket(Bucket=bucket_name)

s3_client = boto3.client('s3')

file_lst = os.listdir('../data/')

for elem in file_lst:
    s3_client.upload_file(f'../data/{elem}', bucket_name, elem)