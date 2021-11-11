from setuptools import setup, find_packages

setup(
    name="neos",
    description="A commandline app for communicating with the NEOS Optimization Server API.",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click"
    ],
    author="Sebastian Baltser",
    author_email="sebastian.baltser@gmail.com",
    python_requires=">=2",
    entry_points={
        "console_scripts": ["neos = neos.scripts.main:neos"]
    }
)