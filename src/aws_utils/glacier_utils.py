from subprocess import Popen, PIPE

def authorize(aws_access_key_id, aws_secret_access_key, aws_session_token):
    """
    authorize checks AWS credentials - if authenticated returns True, else initiates login sequence

    :param aws_access_key_id: the AWS access key part of your credentials
    :type aws_access_key_id: str
    :param aws_secret_access_key: the AWS secret access key part of your credentials
    :type aws_secret_access_key: str
    :param aws_session_token: the session token part of your credentials
    :type aws_session_token: str
    :return: True if authenticated
    :rtype: Optional[bool]
    """    

    check_credentials_command = ["aws sts get-caller-identity"]
    check_credentials_process =  Popen(check_credentials_command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    
    if not check_credentials_process.stderr.read():
        check_credentials_process.stdout.flush()
        check_credentials_process.stderr.flush()
        return True

    command = [f"aws configure set aws_access_key_id {aws_access_key_id}",
                f"aws configure set aws_secret_access_key {aws_secret_access_key}",
                "aws configure set region us-east-1",
                f"aws configure set aws_session_token {aws_session_token}"]
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    process.wait()

    process.stdin.flush()
    process.stdout.flush()
    process.stderr.flush()
    
def restore_object(key, days, bucket='digpath-data'):
    """
    restore_object restores an object in Amazon S3 from Glacier to Standard

    :param key: object key for which image/object to restore
    :type key: str
    :param days: how many days the object should be restored for (after this time period, the object will go back into glacier)
    :type days: int
    :param bucket: the name of the bucket containing the object to restore
    :type bucket: str
    :return: stderr if an error occurs when running the command
    :rtype: Optional[IO[str]]
    """    

    command = [f"aws s3api restore-object --restore-request Days={days} --bucket {bucket} --key {key}"]
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    process.wait()

    if process.stderr.read():
        return process.stderr
        
    process.stdin.flush()
    process.stdout.flush()
    process.stderr.flush()

    # for line in process.stderr:
    #     print(line)

def status_update(key, bucket='digpath-data'):
    """
    status_update sends a HEAD request to get the status of object restoration

    :param key: object key for which image/object to restore
    :type key: str
    :param bucket: the name of the bucket containing the object to restore
    :type bucket: str
    :return: stderr if an error occurs when executing command, else returns stdout
    :rtype: Optional[IO[str]]
    """    

    command = [f"aws s3api head-object --bucket {bucket} --key {key}"]
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    process.wait()

    if process.stderr.read():
        return process.stderr

    process.stdin.flush()
    process.stderr.flush()

    return process.stdout

# status_update(key='Glacier/84440T_001.tif')
# restore_object(key='Glacier/84440T_001.tif', days=1)