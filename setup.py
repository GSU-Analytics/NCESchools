from setuptools import setup, find_packages

setup(
    name="NCEShools",
    version="0.1.4",
    author="Isaac Kerson",
    author_email="ikerson@gsu.edu",
    description="A package to search and extract school details from the NCES website.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GSU-Analytics/NCEShools",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
