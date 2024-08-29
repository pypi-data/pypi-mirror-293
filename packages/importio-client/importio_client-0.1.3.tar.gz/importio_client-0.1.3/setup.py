from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="importio-client",
    version="0.1.3",
    author="Nick Dekker",
    author_email="",
    description="A client library for interacting with the ImportIO API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickdkr/import-io-hook",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    include_package_data=True,
    package_data={
        "importio_client": ["LICENSE"],
    },
)