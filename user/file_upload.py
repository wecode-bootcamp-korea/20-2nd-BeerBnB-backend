from my_settings import AWS_STORAGE_BUCKET_NAME

def s3_upload(client, file):
    client.upload_fileobj(
        file,
        AWS_STORAGE_BUCKET_NAME,
        f'profile/{file}',
        ExtraArgs={
            "ContentType": file.content_type
        })