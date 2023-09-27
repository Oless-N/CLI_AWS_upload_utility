import argparse

from .upload import ZipUploader


def main():
    parser = argparse.ArgumentParser(
        description='upload zip file to s3 with concurency',
    )
    parser.add_argument(
        '--url',
        help='url to ZIP-file',
    )
    parser.add_argument(
        '--zip',
        default=None,
        help='path to ZIP-file',
    )
    parser.add_argument(
        '--bucket',
        default='one-t-bucket',
        help='S3 name bucket',
    )
    parser.add_argument(
        '--prefix',
        default='test_bucket',
        help='S3 key prefix',
    )
    parser.add_argument(
        '--concurrency',
        type=int,
        default=5,
        help='concurrency level (default: 5)',
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='verbose mode',
    )

    parser.add_argument(
        '--contain',
        default=False,
        help='view bucket contain',
    )

    args = parser.parse_args()

    uploader = ZipUploader(
        args.bucket,
        args.prefix,
        args.concurrency,
        args.verbose,
    )
    if args.url:
        uploader.process_url_and_upload(args.url)

    if args.contain:
        print(uploader.get_s3_content())


if __name__ == '__main__':
    main()
