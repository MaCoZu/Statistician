from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="statistician",
    version="0.1.0",
    author="Marco Zausch",
    author_email="marcoz@posteo.de",
    description="Statistical tests and data analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaCoZu/statistician",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
    test_suite='tests',
)
