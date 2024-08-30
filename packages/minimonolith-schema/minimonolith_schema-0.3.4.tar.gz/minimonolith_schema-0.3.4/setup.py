from setuptools import setup, find_packages

setup(
    name="minimonolith-schema",
    #version="0.3.3",
    version="0.3.4",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    #author="Matías Haeussler",
    #author_email="matihaeussler@gmail.com",
    description="Validation of data table columns",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/DeepHackDev/minimonolith-schema",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
