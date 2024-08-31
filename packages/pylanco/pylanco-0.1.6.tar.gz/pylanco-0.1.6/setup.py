from setuptools import setup, find_packages

setup(
    name="pylanco",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        'requests',
        'robocorp-log',
        'beautifulsoup4',
        'time'
    ],
)
