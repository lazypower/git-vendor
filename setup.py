import setuptools
from gitvendor.version import Version
from setuptools import find_packages

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',
    'Topic :: Software Development'
]

setuptools.setup(name='git-vendor',
                 version=Version('0.0.1').number,
                 description='Vendor tagged releases from git to $VCS',
                 long_description=open('README.md').read().strip(),
                 author='Charles Butler',
                 author_email='charles.butler@ubuntu.com',
                 url='http://github.com/chuckbutler/git-vendor',
                 py_modules=[],
                 packages=find_packages(),
                 entry_points={
                     'console_scripts': [
                         'git-vendor = gitvendor.cli:main'
                         ],
                     },
                 install_requires=['gitpython', 'jinja2'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='git, vendor',
                 classifiers=CLASSIFIERS)
