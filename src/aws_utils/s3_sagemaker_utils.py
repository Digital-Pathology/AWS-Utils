import logging
import boto3
import sagemaker


class S3SageMakerUtils():
    """
        A class to initiate a s3 sagemaker session
    """

    def __init__(self):
        """
            Initilize a SageMaker Session
        """
        self.session = sagemaker.Session(boto3.session.Session())

    def upload_data(self, path, bucket="digpath-cache", key_prefix="latest"):
        """
            Upload local file or directory to S3

            :param path: path (absolute or relative) of local file or directory to upload
            :type path: str
            :param bucket: name of the s3 bucket to upload to
            :type bucket: str
            :param key_prefix: optional s3 object key name prefix, s3 uses the prefix to create a directory structure for the bucket content
            :type key_prefix: str
        """

        try:
            self.session.upload_data(path, bucket, key_prefix)

        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def download_data(self, path, bucket="digpath-cache", key_prefix="latest"):
        """
            Download local file or directory from S3

            :param path: local path where the file or directory should be downloaded to
            :type path: str
            :param bucket: name of the s3 bucket to download from
            :type bucket: str
            :param key_prefix: optional s3 object key name prefix
            :type str
        """

        try:
            self.session.download_data(path, bucket, key_prefix)
        except Exception as e:
            logging.error(e)
            raise Exception(e)
