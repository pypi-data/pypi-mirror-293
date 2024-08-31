# setup.py

from setuptools import setup, find_packages

setup(
    name='PrymePython',
    version='0.0.11',
    packages=find_packages(include=['Pryme', 'Pryme.*']),
    description='A python package for prime number utilities.',
    author='Kidus F.mariam Ayalew',
    author_email='kidusfmariamayalew@gmail.com',
    url='https://github.com/kidusfmariam/Pryme',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'sympy',
    ],
    license="MIT",
    python_requires='>=3.6',
    package_data={
    '': ['*.md', '*.txt'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
