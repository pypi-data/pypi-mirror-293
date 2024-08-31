from setuptools import setup, find_packages

setup(
    name='TestMailHelper',
    version='0.2.0',
    packages=find_packages(include=['testmailhelper', 'testmailhelper.*']),
    install_requires=[
        'requests',
    ],
    description='A Python package for interacting with the Testmail.app API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Add this line
    author='Muhammad Ali',
    author_email='muhammad_ali@workmail.com',
    url='https://github.com/tensor35/TestMailHelper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
