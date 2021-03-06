import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='s2e-gui',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple GUI to run and display S2E analysis',
    long_description=README,
    url='https://github.com/dslab-epfl/s2e2-gui',
    author='Davide Di Dio',
    author_email='davide.didio@epfl.ch',
    install_requires=[
        'django',
        'pydot',
        'pyyaml',
        'r2pipe',
        's2e-env',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
