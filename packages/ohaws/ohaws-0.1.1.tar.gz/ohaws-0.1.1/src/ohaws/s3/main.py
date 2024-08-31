import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from typing import Optional


class S3ObjectNotFoundError(Exception):
    """Exception raised when the S3 object is not found."""

    pass


class S3AccessDeniedError(Exception):
    """Exception raised when access to the S3 bucket is denied."""

    pass


class S3UnknownError(Exception):
    """Exception raised for unknown S3 errors."""

    pass


def get_object_and_sign_url(
    object_path: str,
    bucket: str,
    region: Optional[str] = "us-east-1",
    signature_version: Optional[str] = "s3v4",
) -> Optional[str]:
    """
    Generate a pre-signed URL for an S3 object if it exists.

    Parameters:
        object_path (str): The path (key) of the object in the S3 bucket.
        bucket (str): The name of the S3 bucket.
        region (Optional[str]): The AWS region where the bucket is located. Defaults to 'us-east-1'.
        signature_version (Optional[str]): The signature version to use. Defaults to 's3v4'.

    Returns:
        Optional[str]: A pre-signed URL for the S3 object if it exists, or None if an error occurs.

    Raises:
        S3ObjectNotFoundError: If the object is not found.
        S3AccessDeniedError: If access to the bucket is denied.
        S3UnknownError: For any other unknown errors.

    Example:
        url = get_object_and_sign_url('myfolder/myfile.txt', 'mybucket')
        if url:
            print("Access your file here:", url)
    """
    s3_client = boto3.client(
        "s3", config=Config(signature_version=signature_version), region_name=region
    )
    try:
        s3_client.head_object(Bucket=bucket, Key=object_path)

        response = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": object_path}
        )
        return response
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            raise S3ObjectNotFoundError(f"Item not found: {e}")
        elif error_code == "403":
            raise S3AccessDeniedError(f"Bucket doesn't exist or access denied: {e}")
        else:
            raise S3UnknownError(f"Unknown error occurred: {e}")
