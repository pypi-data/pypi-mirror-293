from setuptools import setup, find_packages

setup(
    name='ccrex',
    version='0.3.3',
    description='A module for predicting on protein sequences using CCREx models. \n For more info visit: \n https://github.com/donEnno/ccrex',
    author='Enno Belz',
    author_email='enno.belz@outlook.com',
    url='https://github.com/donEnno/ccrex',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tensorflow',
        'keras',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.9',
)