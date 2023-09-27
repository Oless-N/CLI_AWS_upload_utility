from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='CLI_AWS_upload_utility',
    version='0.0.1',
    author='Oless_N',
    author_email='korklal@gmail.com',
    description='CLI_AWS_upload_utility',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'uploader=uploader:main.main',
        ],
    },
)
