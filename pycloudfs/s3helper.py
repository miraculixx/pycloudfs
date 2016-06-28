import os

import boto3
from boto.s3.connection import S3Connection
from botocore.exceptions import ClientError


class S3Helper(object):
    """
    A simple s3 client
    """
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 bucket='', path=None):
        AWS_ACCESS_KEY_ID = aws_access_key_id or os.environ.get(
            'AWS_ACCESS_KEY_ID', '')
        AWS_SECRET_ACCESS_KEY = aws_secret_access_key or os.environ.get(
            'AWS_ACCESS_KEY_ID', '')
        opts = dict(
            service_name='s3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # removign session as it is not really required
        # self.session = boto3.Session(**opts)
        self.client = boto3.client(**opts)
        self.connection = S3Connection(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        self.bucket = bucket
        self.prefix = path

    def get_list(self, basenames=False):
        bucket = self.connection.get_bucket(self.bucket)
        resp = bucket.list(self.prefix)
        if basenames:
            return [str(os.path.basename(obj.name)) for obj in resp]
        return [str(obj.name) for obj in resp]

    def upload_file(self, filename):
        key = '%s/%s' % (self.prefix, os.path.basename(filename))
        return self.client.upload_file(filename, self.bucket, key)

    def download_file(self, filename, location='./'):
        key = '%s/%s' % (self.prefix, os.path.basename(filename))
        try:
            if location is not None:
                lfile = '%s/%s' % (location, os.path.basename(filename))
                return self.client.download_file(self.bucket, key, lfile)
            return self.client.download_file(
                self.bucket, key, location+filename)
        except ClientError, e:
            raise e
