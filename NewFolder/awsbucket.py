import boto3

ACCESS_KEY = "AKIAQCQW67YWUCSCEMHF"
ACCESS_SECRET = "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"
BUCKET_NAME = "images.lastevents.space"

class AwsS3:

    def __init__(self) -> None:
        self.s3Client = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=ACCESS_SECRET)

    def upload_in_s3_obj(self, fileobj, objname):
        self.s3Client.upload_fileobj(fileobj, BUCKET_NAME, objname, ExtraArgs={'ACL':'public-read'})

    def upload_in_s3(self, filename, objname):
        self.s3Client.upload_file(filename, BUCKET_NAME, objname, ExtraArgs={'ACL':'public-read'})
