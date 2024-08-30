import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrypted_sdk",
    version="0.0.0",
    author="Koushik Dutta",
    author_email="koushd@gmail.com",
    description="scrypted",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koush/scrypted",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)