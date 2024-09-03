from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='treefolder',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'treefolder=treefolder.tree:main',
        ],
    },
    author='Alberto Perez Ortega',
    author_email='apo0106@gmail.com',
    description='A simple Python program that generates an ASCII representation of a directory tree.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Aperezortega/Treefolder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)