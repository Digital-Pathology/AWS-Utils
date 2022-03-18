from subprocess import Popen, PIPE

def authorize(aws_access_key_id, aws_secret_access_key, aws_session_token):
    """
        Checks AWS credentials - if authenticated returns True, else initiates login sequence
        Parameters:
            aws_access_key_id (string): the AWS access key part of your credentials
            aws_secret_access_key (string): the AWS secret access key part of your credentials
            aws_session_token (string): the session token part of your credentials
        Returns:
            True if authenticated
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
        Restores an object in Amazon S3 from Glacier to Standard
        Parameters:
            key (string): object key for which image/object to restore
            days (integer): how many days the object should be restored for (after this time period,
                           the object will go back into glacier)
            bucket (string): the name of the bucket containing the object to restore
        Returns:
            stderr if an error occurs when running the command
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
        Sends a HEAD request to get the status of object restoration
        Parameters:
            key (string): object key for which image/object to restore
            bucket (string): the name of the bucket containing the object to restore
        Returns:
            stderr if an error occurs when executing command, else returns stdout
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
