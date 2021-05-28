from my_settings import AWS_STORAGE_BUCKET_NAME

class S3Client:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    def upload(self, file, file_name):
        self.s3_client.upload_fileobj(
            file,
            AWS_STORAGE_BUCKET_NAME,
            f"profile/{file_name}",                
            ExtraArgs={"ContentType": file.content_type}
       ) 
    def delete(self, file_name):
        self.s3_client.delete_object(
            Bucket=AWS_STORAGE_BUCKET_NAME, 
            Key=file_name)