from setuptools import find_packages, setup

setup(
    name="access_db_easy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyodbc",
    ],
    author="ThAnToI",
    author_email="thienphuoc08@gmail.com",
    description="A simple library to interact with Access databases",
    url="https://github.com/ThAnToI/PyPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
