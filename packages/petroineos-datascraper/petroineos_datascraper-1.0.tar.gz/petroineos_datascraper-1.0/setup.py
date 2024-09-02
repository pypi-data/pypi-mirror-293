from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="petroineos_datascraper",  # Replace with your own package name
    version="1.0",
    author="Assad Khan",
    author_email="assad.beta@gmail.com",
    description="Scrapes energy data from UK gov website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/programmatick/datascraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python"
    ],
    python_requires='>=3.7',
)
