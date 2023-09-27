
import pytest

from uploader.upload import ZipUploader


@pytest.fixture
def zip_uploader():
    yield ZipUploader(
        bucket='test',
        prefix='test_prefix',
    )


@pytest.mark.vcr
def test_download_file_from_web_server(zip_uploader):
    res = zip_uploader.process_url_and_upload(
        f'https://www.learningcontainer.com/download/sample-zip-files/?wpdmdl=1637&refresh=65118c7fa61b71695648895',
    )

    assert res


@pytest.mark.vcr
def test_download_zip_from_url_failure(zip_uploader):
    url = 'http://example.com/fake.zip'
    result = zip_uploader.process_url_and_upload(url)

    assert not result
