#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: suralmasha - Badasyan Alexandra

from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f_requirements:
        deps = []
        while True:
            row = f_requirements.readline()
            if row == '':
                break
            elif row.startswith('--'):
                continue
            elif row.startswith('-e'):
                url, name = row.split('#egg=')
                row = name.replace('\n', '') + ' @' + url.replace('-e', '')
            deps.append(row)
        return deps


def readme():
    with open('README.md', 'r', encoding='utf-8') as f_readme:
        return f_readme.read()


if __name__ == "__main__":
    setup(
        name='phonetic_diversity',
        # version='0.1.0',
        description='A metric of phonetic diversity and balance of textual data.',
        long_description=readme(),
        url='https://github.com/suralmasha/PhonDB',
        classifiers=[
            'Natural Language :: Russian',
            'Programming Language :: Python :: 3.8',
            'Topic :: Text Processing :: Linguistic :: NLP'
        ],
        author='Badasyan Alexandra',
        keywords='nlp russian phonetics linguistic voice tts asr',
        author_email='sashabadasyan@icloud.com',

        packages=find_packages(exclude=['example.py'],),
        # package_data={'phonetic_diversity': []},
        include_package_data=True,
        install_requires=requirements(),
        zip_safe=False
    )
