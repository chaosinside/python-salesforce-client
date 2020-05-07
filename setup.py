import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SalesforceClient",
    version="1.0.3",
    author="Chris Hubbard",
    author_email="chubbard@gmail.com",
    description="A python client for Salesforce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chaosinside/python-salesforce-client",
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)