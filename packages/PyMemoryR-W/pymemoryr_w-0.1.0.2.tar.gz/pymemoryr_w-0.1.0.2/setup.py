from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyMemoryR-W',
    version='0.1.0.2',
    author='Mahd Hasan Shuvo',
    author_email='shuvobbhh@gmail.com',
    description='A library for manipulating memory in a Windows process',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Ensure this matches your file format
    url='https://github.com/Mahdi-hasan-shuvo/PyMemoryRW',
    packages=find_packages(include=['mahdix', 'pymem', 'ctypes', 'pyinjector']),
    install_requires=[
        'pywin32',
        'pyinjector',
        'pymem',
        'ctypes',
        'mahdix',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
