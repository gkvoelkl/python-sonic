from setuptools import setup
# To use a consistent encoding
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'python-osc',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]


setup(
    name='python-sonic',
    version='0.4.3',
    description='Programming Music with Sonic Pi or Supercollider',
    long_description=long_description,
    url='https://github.com/gkvoelkl/python-sonic',
    author='gkvoelkl',
    author_email='gkvoelkl@nelson-games.de',
    packages=[
        'psonic',
        'psonic.samples',
        'psonic.samples.loops',
        'psonic.internals',
    ],
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
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
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
