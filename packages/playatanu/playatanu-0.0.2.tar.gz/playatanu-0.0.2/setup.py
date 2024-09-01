from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
]

setup(
    name='playatanu',
    version='0.0.2',
    description='machine learning toolkit',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Atanu Debnath', 
    author_email='playatanu@gmail.com',
    license='MIT',
    classifiers = classifiers,
    packages=find_packages(),
    insall_requires=['torch']
    
)