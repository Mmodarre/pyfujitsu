import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfujitsu",
    version="0.7.1.3",
    author="Mehdi Modarressi",
    author_email="Luckposht@gmail.com",
    description="Python library to control Fujitsu General Airconditioners on AylaNetworks IoT platform",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/Mmodarre/pyfujitsu",
    packages=setuptools.find_packages(),
    install_requires=['requests','certifi','chardet','idna','urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
