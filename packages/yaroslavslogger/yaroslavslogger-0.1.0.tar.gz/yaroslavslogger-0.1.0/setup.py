from setuptools import setup, find_packages

setup(
    name='yaroslavslogger',
    version='0.1.0',
    author='YaroslavS',
    author_email='yarosmr@gmail.com',
    description='A simple logging helper for Python projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

