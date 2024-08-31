import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "LatinDeckCreator",
    version = "0.0.3",
    author = "Forrest Zeng",
    author_email = "forrestzengmusic@gmail.com",
    description = ("A package using pywhitakers to create Latin flashcard decks."),
    license = "Apache 2.0",
    keywords = "Latin translation whitakers flashcards",
    long_description=read('README.md'),
    packages=find_packages(),
    install_requires=read("requirements.txt").splitlines()
)
