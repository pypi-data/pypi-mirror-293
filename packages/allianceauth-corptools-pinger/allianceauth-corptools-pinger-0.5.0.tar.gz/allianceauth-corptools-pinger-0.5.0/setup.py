from pinger import __version__
import os
from setuptools import find_packages, setup
install_requires = [
    'allianceauth>=2.9.0',
    'allianceauth-corptools>=2.1.2'
]
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='allianceauth-corptools-pinger',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    license='GNU General Public License v3 (GPLv3)',
    description='Alliance Auth Plugin',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools-pinger',
    author='AaronKable',
    author_email='aaronkable@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
