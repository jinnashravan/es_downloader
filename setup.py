from __future__ import print_function
from __future__ import division

from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

install_requirements = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='es-downloader',
    version='0.2.5',
    description='Command line tool for download resources from elastic search',
    long_description=readme,
    author='Hamed Saljooghinejad',
    author_email='hamed.saljooghinejad@onfido.com',
    url='https://bitbucket.org/onfido/es-downloader/',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'es-downloader = es_downloader.main:main', ], },
    keywords=['python', 'es', 'download', 'binaries', 'resources',
              'downloader'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
