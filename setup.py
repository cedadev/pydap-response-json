import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    setup(
        name = 'pydap-response-json',
        version = '0.0.1',
        description = 'JSON response type for PyDAP',
        classifiers = [
            "Programming Language :: Python",
        ],
        author = 'Matt Pryor',
        author_email = 'matt.pryor@stfc.ac.uk',
        url = 'https://github.com/cedadev/pydap-response-json',
        keywords = 'pydap response json',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = ['pydap'],
        entry_points="""
            [pydap.response]
            json = pydap.responses.json:JSONHandler
        """,
    )
