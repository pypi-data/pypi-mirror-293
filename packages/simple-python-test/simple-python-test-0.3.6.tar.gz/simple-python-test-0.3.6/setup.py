from setuptools import setup, find_packages
import sys

__version__ = "0.3.6"

setup(
    name="simple-python-test",
    version=__version__,
    url="https://github.com/SimpleDataLabsInc/dummy",
    packages=find_packages(exclude=["test.*", "test"]),
    description="Helper library for prophecy generated code",
    long_description=open("README.md").read(),
    install_requires=[],
    keywords=["python", "prophecy"],
    classifiers=[],
    zip_safe=False,
    license="GPL-3.0",
)
