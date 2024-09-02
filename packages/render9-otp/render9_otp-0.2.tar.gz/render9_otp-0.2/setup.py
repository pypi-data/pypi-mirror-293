# setup.py
from setuptools import setup, find_packages

setup(
    name='render9_otp',  # The name of your package
    version='0.2',  # The initial release version
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[  # External dependencies the package needs to run
        'requests',
        'python-dotenv',
    ],
)
