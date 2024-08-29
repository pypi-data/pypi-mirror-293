from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="importio-client",
    version="0.2.3",
    author="Nick Dekker",
    author_email="",
    description="A client library for interacting with the ImportIO API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickdkr/importio-client",
    project_urls={
        "Bug Tracker": "https://github.com/nickdkr/importio-client/issues",
        "Source Code": "https://github.com/nickdkr/importio-client",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
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
    extras_require={
        "test": ["pytest>=6.0"],
    },
)