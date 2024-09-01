from setuptools import setup


setup(
    name='SensorMiddleware',
    version='1.6',
    author_name='Pablo Skubert',
    author_email='pablo1920@protonmail.com',

    packages=['app'],
    install_requires=[
        "boto3==1.33.13",
        "botocore==1.33.13",
        "certifi==2024.2.2",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "colorama==0.4.6",
        "Flask==2.2.5",
        "idna==3.6",
        "importlib-metadata==6.7.0",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.3",
        "jmespath==1.0.1",
        "markdown-it-py==2.2.0",
        "MarkupSafe==2.1.5",
        "mdurl==0.1.2",
        "psutil==5.9.8",
        "Pygments==2.17.2",
        "python-dateutil==2.9.0.post0",
        "requests==2.31.0",
        "requests-toolbelt==1.0.0",
        "rich==13.7.1",
        "s3transfer==0.8.2",
        "shellingham==1.5.4",
        "six==1.16.0",
        "typer==0.12.1",
        "typer-slim==0.12.1",
        "urllib3==1.26.18",
        "Werkzeug==2.2.3",
        "zipp==3.15.0"
    ],
    description='Middleware para os Sensores EcoTrust',
    long_description=open('README.md', 'r').read(),
    entry_points={
        'console_scripts': [
            'scontroler = app.main:scontroler_main'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
