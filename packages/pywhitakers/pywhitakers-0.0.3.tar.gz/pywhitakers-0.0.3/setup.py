import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pywhitakers",
    version = "0.0.3",
    author = "Forrest Zeng",
    author_email = "forrestzengmusic@gmail.com",
    description = ("An API package to latin-words.com that returns the most likely Latin translation of a word."),
    license = "Apache 2.0",
    keywords = "Latin translation whitakers",
    long_description=read('README.md'),
    install_requires=[
        "requests",
        "unidecode"
    ]
)