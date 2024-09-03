# setup.py

from setuptools import setup, find_packages

setup(
    name="pandas_profiling_manual",
    version="0.1.0",
    author="Subham Subhash Dalmia",
    author_email="subhamsdalmia@gmail.com",
    description="A manual data profiling tool built with Pandas",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pandas_profiling_manual",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.1.0",
        "seaborn>=0.10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
