
from setuptools import setup, find_packages

setup(
    name="holosen-unit-converter",
    version="0.1.0",
    author="Hossein Badrnezhad",
    author_email="holosenpythonknight@gmail.com",
    description="A simple Python library to convert between different units",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/badrnezhad/unit-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
