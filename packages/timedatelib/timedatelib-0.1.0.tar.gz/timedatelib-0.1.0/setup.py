# setup.py
from setuptools import setup, find_packages

setup(
    name='timedatelib',  # Your library name
    version='0.1.0',  # Initial version
    author='Your Name',
    author_email='youremail@example.com',
    description='A library for time and date functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/timedatelib',  # Link to your project repository
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
	
