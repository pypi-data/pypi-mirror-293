
### 6. `setup.py`

#Create a `setup.py` file to define your package metadata and dependencies:

#```python
from setuptools import setup, find_packages

setup(
    name='f_program',
    version='0.3',
    packages=find_packages(),
    author='arasu',
    author_email='arasum6262@gmail.com',
    description='A package for Gaussian and Multinomial Naive Bayes classification.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
