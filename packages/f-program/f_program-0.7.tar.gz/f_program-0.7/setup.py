# setup.py

from setuptools import setup, find_packages

setup(
    name='f_program',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'f_program_download=f_program.__main__:main',
        ],
    },
)
