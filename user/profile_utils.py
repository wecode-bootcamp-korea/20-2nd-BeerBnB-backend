from my_settings import AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN

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
        file_urls = f"https://{AWS_S3_CUSTOM_DOMAIN}/profile/{file_name}"

        return file_urls
        
    def delete(self, file_name):
        self.s3_client.delete_object(
            Bucket=AWS_STORAGE_BUCKET_NAME, 
            Key=file_name)