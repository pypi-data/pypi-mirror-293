# coding: utf-8

"""
    Safe Checkout

    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.

    The version of the OpenAPI document: 2.0.24
    Contact: noc@tripartie.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "tpdk-safe-checkout"
VERSION = "2.0.24"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Safe Checkout",
    author="Tripartie SAS",
    author_email="noc@tripartie.com",
    url="https://pypi.org/project/tpdk-safe-checkout",
    keywords=["OpenAPI", "OpenAPI-Generator", "Safe Checkout"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    Simple, yet elegant web interfaces for your convenience. One request away from your first secured C2C transaction.
    """,  # noqa: E501
    package_data={"tpdk_safe_checkout": ["py.typed"]},
)
