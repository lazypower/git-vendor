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
                 version=Version('0.0.3').number,
                 description='Vendor tagged releases from git to $VCS',
                 long_description=open('README.md').read().strip(),
                 author='Charles Butler',
                 author_email='charles.butler@ubuntu.com',
                 url='http://github.com/chuckbutler/git-vendor',
                 download_url='https://github.com/chuckbutler/git-vendor/releases/',
                 py_modules=[],
                 packages=find_packages(),
                 entry_points={
                     'console_scripts': [
                         'git-vendor = gitvendor.cli:main'
                         ],
                     },
                 install_requires=['gitpython', 'jinja2', 'pyyaml', 'path.py',
                                   'dirsync', 'six'],
                 package_data={
                     'template': ['template/vendor-rc'],
                 },
                 include_package_data=True,
                 license='MIT License',
                 zip_safe=False,
                 keywords='git, vendor',
                 classifiers=CLASSIFIERS)
