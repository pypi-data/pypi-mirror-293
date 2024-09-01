from setuptools import setup, find_packages

setup(
    name="testHelloWorldpkg",
    version="0.0.5",
    author="Moshiur",
    author_email="",
    description="A Hello world pkg",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",  # Replace with your GitHub repository URL
    packages=find_packages(),
    include_package_data=True,

 
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with the appropriate license if necessary
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',  # Adjust this based on your project's Python version compatibility
)


