from setuptools import setup, find_packages, Extension

setup(
    name='obfusguard',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['data/*.pkl'],  # Include binary files
    },
    description='A non-cryptographic multi-layered Encoding and Hashing algorithm.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rajnish Tripathi',
    url='https://github.com/RajnishXCode/ObfusGuard',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
