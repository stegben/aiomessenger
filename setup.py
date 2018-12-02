from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

REQUIRED_PACKAGES = []


setup(
    name="aiomessenger",
    version="0.1.0",
    description=long_description,
    author="cph",
    author_email="stegben.benjamin@gmail.com",
    url="https://github.com/stegben/messenger-api-py",
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)
