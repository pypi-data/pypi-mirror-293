from setuptools import setup,find_packages

with open("README.md","r") as file:
    description=file.read()

setup(
    name="StefanTools",
    version="1.2.3",
    packages=find_packages(),
    install_requires=[
        "rich",
        "inputimeout"
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)