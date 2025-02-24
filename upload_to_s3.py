
"""
"""
#%%
import boto3
import os
from dotenv import load_dotenv
#%%
# Load environment variables from .env file
load_dotenv()

# Retrieve credentials and other variables from environment
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")
s3_bucket = os.getenv("S3_BUCKET_NAME")

# Debug print
print(f"AWS_ACCESS_KEY_ID: {aws_access_key}")
print(f"AWS_SECRET_ACCESS_KEY: {'SET' if aws_secret_key else 'NOT SET'}")  # Don't print actual secret
print(f"AWS_REGION: {aws_region}")


#%%
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)

#%%

def upload_to_s3(folder_dir, s3_bucket):
    """
    
    """
    files = os.listdir("downloads")

    for ifile in files:
        # Upload file
        try:
            file_path = os.path.join(folder_dir, ifile)
            s3.upload_file(file_path, s3_bucket, file_path)
            print(f"File uploaded to s3://{s3_bucket}/{s3_key}")
        except Exception as e:
            print(f"Failed to upload file: {e}")

os.listdir("downloads")

#%%
if __name__ == "__main__":
    # Upload file to S3
    upload_to_s3(folder_dir="downloads",s3_bucket= s3_bucket)

# %%
