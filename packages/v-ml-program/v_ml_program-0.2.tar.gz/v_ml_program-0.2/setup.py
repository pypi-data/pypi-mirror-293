# setup.py
from setuptools import setup, find_packages

setup(
    name='v_ml_program',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    description='A package for Iris and text classification',
    author='Arasu',
    author_email='arasum6262@gmail.com',
)
