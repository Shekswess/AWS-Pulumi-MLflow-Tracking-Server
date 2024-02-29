import logging

from pulumi_aws import s3

logger = logging.getLogger("s3")
logger.setLevel(logging.INFO)


def create_s3_bucket(name: str, acl: str = "private") -> s3.Bucket:
    """
    Create an S3 bucket
    :param name: The name of the bucket
    :param acl: The access control list
    :return: The S3 bucket
    """
    try:
        logger.info(f"Creating S3 bucket: {name}")
        bucket = s3.Bucket(name, acl=acl)
        return bucket
    except Exception as error:
        logger.error(f"Error creating S3 bucket: {error}")
        raise error
