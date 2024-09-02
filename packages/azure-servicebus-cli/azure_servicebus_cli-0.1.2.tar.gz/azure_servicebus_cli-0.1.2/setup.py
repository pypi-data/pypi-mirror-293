from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="azure-servicebus-cli",
    version="0.1.2",
    author="Mustafa Hakimi",
    author_email="mustafa.hakimi94@gmail.com",
    description="A CLI tool for interacting with Azure Service Bus Queues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/azure-servicebus-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "azure-servicebus>=7.0.0",
    ],
    entry_points={
        'console_scripts': [
            'azsb=azure_servicebus_cli.cli:main',
        ],
    },
)
