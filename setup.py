#!/usr/bin/env python3
import setuptools


setuptools.setup(
    name='filefind',
    version='0.1.0',

    author='Aurélien Gâteau',
    author_email='mail@agateau.com',

    description='An easy-to-use, source-code friendly file finder',
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'ff = filefind.main:main'
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
