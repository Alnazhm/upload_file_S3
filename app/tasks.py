from celery import shared_task
from botocore.exceptions import NoCredentialsError
import boto3
import io
import threading
from operator import itemgetter

@shared_task
def upload_large_file_to_s3(file_data, s3_bucket, s3_key):
    s3 = boto3.client('s3')

    try:
        response = s3.create_multipart_upload(Bucket=s3_bucket, Key=s3_key)
        upload_id = response['UploadId']
        part_size = 100 * 1024 * 1024

        def upload_part(part_data, part_number):
            try:
                response = s3.upload_part(
                    Bucket=s3_bucket,
                    Key=s3_key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=part_data
                )
                return {'PartNumber': part_number, 'ETag': response['ETag']}
            except Exception as e:
                return None

        parts = []
        part_number = 1
        file_data = io.BytesIO(file_data)
        threads = []

        while True:
            part = file_data.read(part_size)
            if not part:
                break
            thread = threading.Thread(target=lambda p=part, pn=part_number: parts.append(upload_part(p, pn)))
            threads.append(thread)
            thread.start()
            part_number += 1


        for thread in threads:
            thread.join()

        parts = [part for part in parts if part]
        parts = sorted(parts, key=itemgetter('PartNumber'))
        s3.complete_multipart_upload(Bucket=s3_bucket, Key=s3_key, UploadId=upload_id, MultipartUpload={'Parts': parts})
    except NoCredentialsError:
        print("Не настроены AWS S3 Storage")












