from setuptools import setup, find_packages

setup(
    name='playatanu',
    version='0.0.1',
    description='machine learning toolkit',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),

    author='Atanu Debnath', 
    author_email='playatanu@gmail.com',

    license='MIT',
    
    packages=find_packages(),
    insall_requires=['torch']
    
)