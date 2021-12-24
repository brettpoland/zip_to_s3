import pyminizip
import boto3
import uuid

input_file = "test.txt"

def compress(file):
    pre = None
    output_file = "output_test.zip"
    password = "12345"
    com_lvl = 5
    pyminizip.compress(file, None, output_file, password, com_lvl)
    return output_file


compress(input_file)

output_file = compress(input_file)

s3_resource = boto3.resource('s3')



def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])
bucket_id = create_bucket_name('s3bucketbackup')


def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

second_bucket_name, second_response = create_bucket(bucket_prefix='secondbucket', s3_connection=s3_resource)

s3_resource.Object(second_bucket_name, output_file).upload_file(
    Filename=output_file)