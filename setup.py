from setuptools import setup, find_packages

setup(
    name="statistician",
    version="0.1.0",
    author="Marco Zausch",
    author_email="your.email@example.com",
    description="Statistical tests",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MaCoZu/statistician",  
    packages=find_packages(),
    install_requires=[
        "scipy.stats",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
