from setuptools import setup


print("TEST")
setup(
    name='SensorMiddleware',
    version='1.0',
    author_name='Pablo Skubert',
    author_email='pablo1920@protonmail.com',

    packages=['app'],
    install_requires=[
        'boto3',
        'requests'
    ],
    description='Middleware para os Sensores EcoTrust',
    long_description=open('README.md', 'r').read(),
    entry_points={
        'console_scripts': [
            'scontroler = app:main'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
