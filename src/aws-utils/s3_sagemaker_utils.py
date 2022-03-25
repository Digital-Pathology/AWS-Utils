import logging
import boto3
import sagemaker

class S3SageMakerUtils():
    """
        A class to initiate a s3 sagemaker session
        Methods:
            upload_data(path, bucket="digpath-cache", key_prefix="latest"): upload local file or directory to S3
            download_data( path, bucket="digpath-cache", key_prefix="latest"): download local file or directory from S3
    """

    def __init__(self):
        """
            Initilize a SageMaker Session
        """
        self.session = sagemaker.Session(boto3.session.Session())

    def upload_data(self, path, bucket="digpath-cache", key_prefix="latest"):
        """
            Upload local file or directory to S3
            Parameters:
                path (string): path (absolute or relative) of local file or directory to upload
                bucket (str): name of the s3 bucket to upload to
                key_prefix (str): optional s3 object key name prefix, s3 uses the prefix to create 
                                  a directory structure for the bucket content
        """

        try:
            self.session.upload_data(path, bucket, key_prefix)

        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def download_data(self, path, bucket="digpath-cache", key_prefix="latest"):
        """
            Download local file or directory from S3
            Parameters:
                path (string): local path where the file or directory should be downloaded to
                bucket (str): name of the s3 bucket to download from
                key_prefix (str): optional s3 object key name prefix
        """

        try:
            self.session.download_data(path, bucket, key_prefix)
        except Exception as e:
            logging.error(e)
            raise Exception(e)
