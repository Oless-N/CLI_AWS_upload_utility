# uploader

uploader is a command-line utility for uploading ZIP archives to Amazon S3 with concurrency.

### Installation

Install using `pip`:

    ```pip install .```

After installing uploader, you can use it from the command line to upload ZIP archives to Amazon S3.

` uploader --url=https://www.learningcontainer.com/download/sample-zip-files/\?wpdmdl\=1637\&refresh\=65118c7fa61b71695648895`

### Command-Line Parameters

`--url`: _The link to the ZIP file you want to upload._

`--bucket your_bucket`: _The name of the S3 bucket (default: one-t-bucket)._

`--prefix your_prefix`: _The S3 key prefix (default: pr_1)._

`--concurrency number_of_threads`: _Concurrency level (default: 5)._

`--verbose`: _Enable verbose mode (enabled by default)._

`--contain=1`: _Show contain bucket_  

### Environment Variables via .env File
To configure AWS storage and other parameters, you can use environment variables 
via a .env file. Create a .env file in the root folder 
of your project and add the following variables:

### .env file

    AWS_ACCESS_KEY_ID=your_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY=your_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION=your_AWS_DEFAULT_REGION

uploader will automatically use these variables when uploading files to Amazon S3.

### Example

```uploader /path_to_file.zip --bucket my-bucket --prefix my-prefix --concurrency 10```

In this example, uploader uploads the specified ZIP file to an 
S3 bucket named my-bucket with 
a prefix key of my-prefix using a concurrency of 10 threads.

_*You can get more information about **uploader** by using the uploader --help command._

