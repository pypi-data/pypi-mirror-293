from setuptools import setup, find_packages

setup(
    name='findNplot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pandas','matplotlib','numpy','twine'],
    author='Sushruta Das',
    author_email='sushrutadas@gmail.com',
    description='A program to access an excel sheet and extract elements of a single column and plot them',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.11',
)