import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand

version = '0.1.0'

install_requires = [
    'sortedcontainers',
    'requests',
    'invoke',
    'jinja2',
    'setuptools'
]

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
]

setup(
    name='easyops',
    version=version,
    description="easily ops",
    url='https://github.com/xxy1991/easyops',
    author="xxy1991",
    author_email='xxy1991@gmail.com',
    license='Apache License 2.0',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(exclude=['tests', 'private*']),
    package_data={'easyops': ['scripts/*', 'templates/**/*']},
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'docs': docs_extras,
    },
    test_suite='easyops',
)
