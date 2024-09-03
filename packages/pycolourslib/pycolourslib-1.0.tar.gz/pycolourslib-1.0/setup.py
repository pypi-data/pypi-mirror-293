from setuptools import setup, find_packages

setup(
    name='pycolourslib',
    version='1.0',
    packages=find_packages(),
    description='a python module with variabled colours for more simplicity and less time-wasting in your projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='QZ-K',
    author_email='kuzeykural040510@gmail.com',
    url='https://github.com/KZed-K/pycolourslib', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
