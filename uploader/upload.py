import os
import shutil
import tempfile
import zipfile
import boto3
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('RERION_NAME'),
)


class ZipUploader:
    def __init__(self, bucket, prefix, concurrency=5, verbose=False):
        self.bucket = bucket
        self.prefix = prefix
        self.concurrency = concurrency
        self.verbose = verbose
        self.s3_client = session.client('s3')
        self.temp_folder = './uploader/ziptmp'
        self.default_zip_name = 'simple.zip'
        if not os.path.exists(self.temp_folder):
            os.mkdir(self.temp_folder)

    def _clean(self):
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder, ignore_errors=True)

    def get_s3_content(self):
        objects = self.s3_client.list_objects(Bucket=self.bucket)
        return [obj['Key'] for obj in objects.get('Contents', [])]

    def _upload_file(self, file_path, s3_key):
        try:
            self.s3_client.upload_file(file_path, self.bucket, s3_key)
            if self.verbose:
                print(f'Success upload {file_path} to S3')
        except Exception as e:
            if self.verbose:
                print(f'Failed upload {file_path}: {str(e)}')

    def _download_zip_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.local_zip_path = f'{self.temp_folder}/{self.default_zip_name}'
            with open(self.local_zip_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return False

    def upload_zip_archive(self, zip_file_path):
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_archive:
                file_list = zip_archive.namelist()

                with ThreadPoolExecutor(max_workers=self.concurrency) as executor: # noqa
                    for file_name in file_list:
                        s3_key = os.path.join(self.prefix, file_name)
                        file_path = zip_archive.extract(
                            file_name,
                            self.temp_folder,
                        )
                        executor.submit(self._upload_file, file_path, s3_key)
        except FileNotFoundError as e:
            print(str(e))
        finally:
            self._clean()

    def process_url_and_upload(self, url):
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        if not file_name:
            file_name = self.default_zip_name
        local_zip_path = f"./{self.temp_folder}/{file_name}"

        if self._download_zip_from_url(url):
            self.upload_zip_archive(local_zip_path)
            return True

        else:
            print(f"Failed to download the ZIP archive from {url}")
            return
