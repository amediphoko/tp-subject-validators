import os
from setuptools import setup, find_packages

'''open and read the README file'''
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

'''allow setup.py to be run from any path'''
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='tp-subject-validators',
    version='0.0.1',
    author='Ame N Diphoko',
    author_email='adiphoko@bhp.org.bw',
    description=('tp subject\'s form validations and tests.'),
    url='https://github.com/amediphoko/tp-subject-validators',
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    zip_safe=False,
    keywords='django trainee program subject tp validators',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
