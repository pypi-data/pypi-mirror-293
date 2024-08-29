# setup.py

from setuptools import setup, find_packages

setup(
    name='PrimoSphere',
    version='0.0.10',
    packages=find_packages(include=['Pryme', 'Pryme.*']),
    description='A python package for prime number utilities.',
    author='Kidus F.mariam Ayalew',
    author_email='kidusfmariamayalew@gmail.com',
    url='https://github.com/kidusfmariam/Pryme',
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
