#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

setup(
    name='scant3r',
    version="0.9.2",
    description='Module based Bug Bounty Automation Tool',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Khaled Nassar',
    author_email='knassar702@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    url='https://github.com/knassar702/scant3r',
    zip_safe=False,
    download_url='https://github.com/knassar702/scant3r/archive/v%s.zip' % "0.9.2",
    packages=find_packages(),
    include_package_data = True,
    package_data={'scant3r':["db/txt/*.txt"]},
    #package_dir={"":"scant3r"},
    install_requires=[
        "rich==12.4.1",
        "requests==2.27.1",
        "colorama==0.4.4",
        "tldextract==3.3.0",
        "fuzzywuzzy==0.18.0",
        "pycryptodome==3.14.1",
        "pyyaml==6.0",
        "flask==2.1.2"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'scant3r = scant3r.__main__:main'
        ]
    },
    keywords=['sectools',"scant3r", 'bug bounty', 'automation', 'pentesting', 'security'],
)
