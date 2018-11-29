import os
import io
import boto3
from pathlib import Path    


def validate_exist_file(filename):
    if not os.path.isfile(filename):
        raise Exception("Archivo input {} no existe.".format(filename))

def get_file_from_s3(bucket_name, bucket_key, filename):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(
        bucket_key, 
        filename
    )

def get_file_from_storage(config, env, storage, input_file):
    if storage == 's3': 
        bucket_name = config['s3']['input']['bucket']
        bucket_key = "{}/{}".format(
            config['s3']['input']['key'],
            input_file
        )
        (env, sub_env) = env.split('.')
        get_file_from_s3(
            bucket_name.format(env=env),
            bucket_key.format(env=env, sub_env=sub_env),
            input_file
        )

def put_file_to_storage(config, env, storage, output_file):
    if storage == 's3': 
        output_filename = Path(output_file).name
        bucket_name = config['s3']['output']['bucket']
        bucket_key = "{}/{}".format(
            config['s3']['output']['key'],
            output_filename
        )
        put_file_to_s3(
            output_file,
            bucket_name.format(env=env),
            bucket_key.format(env=env)
        )

def put_file_to_s3(filename, bucket_name, bucket_key):
    extra_args = {
        'ContentType': 'text/html',
        'ACL':'public-read'
    }
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(
        filename, bucket_name, bucket_key, ExtraArgs=extra_args)
