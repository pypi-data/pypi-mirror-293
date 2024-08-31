from setuptools import setup, find_packages

setup(
    name='TestMailHelper',
    version='0.1.0',
    packages=find_packages(include=['testmailhelper', 'testmailhelper.*']),
    install_requires=[
        'requests',
    ],
    description='A Python package for interacting with the Testmail.app API.',
    author='Muhammad Ali',
    author_email='muhammad_ali@workmail.com',
    url='https://github.com/tensor35/TestMailHelper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
