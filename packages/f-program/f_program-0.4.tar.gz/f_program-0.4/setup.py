from setuptools import setup, find_packages

setup(
    name='f_program',
    version='0.4',  # Incremented version number
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'f_program=f_program:generate_output',
        ],
    },
    author='Arasu',
    author_email='arasum6262@gmail.com',
    description='A package for demonstrating Naive Bayes classification.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
