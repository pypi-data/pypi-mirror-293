from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

LONG_DESCRIPTION = (this_directory / "README.md").read_text()  + '\n\n' + (this_directory / "CHANGELOG.md").read_text()

VERSION = '0.0.5' 
DESCRIPTION = 'machine learning toolkit'

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
]

setup(
    name='playatanu',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Atanu Debnath', 
    author_email='playatanu@gmail.com',
    license='MIT',
    classifiers = classifiers,
    packages=find_packages(),
    url="https://github.com/playatanu/py-playatanu",
    insall_requires=['pytorch']
    
)