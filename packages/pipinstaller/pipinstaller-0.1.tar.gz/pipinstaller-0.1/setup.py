# setup.py

from setuptools import setup, find_packages
setup(
    name="pipinstaller",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "install-from-requirements=pipinstaller.pipinstaller:install_from_requirements",
        ],
    },
    author="Souporno Chakraborty",
    author_email="shrabanichakraborty83@gmail.com",
    description="A package to install banch of  packages from a pypi.org .",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
