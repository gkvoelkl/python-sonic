from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-sonic',
    version='0.1.2',
    description='Programming Music with Sonic Pi or Supercollider',
    long_description=long_description,
    url='https://github.com/gkvoelkl/python-sonic',
    author='gkvoelkl',
    author_email='gkvoelkl@nelson-games.de',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords= [
       'music',
       'sonic pi',
       'raspberry pi',
       'audio',
       'music composition',
       'scsynth',
       'supercollider',
       'synthesis'
    ],

    #packages=find_packages(),
    py_modules=['psonic'],
    install_requires=['pythonosc'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)

