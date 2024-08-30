from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.rst")

setup(
    name = 'collinear',
    version = "0.1.0",
    author = 'Collinear AI',
    author_email = 'info@collinear.ai',
    url = 'https://www.collinear.ai/',
    description = 'A simple example python package.',
    long_description_content_type = "text/x-rst",  # If this causes a warning, upgrade your setuptools package
    long_description = long_description,
    license = "MIT license",
    packages = find_packages(exclude=["test"]),  # Don't include test directory in binary distribution
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # Update these accordingly
)
