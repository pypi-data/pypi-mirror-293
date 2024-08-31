from setuptools import setup, find_packages

setup(
    name='ETHregions2Woredas',
    version='0.1.0',
    packages=find_packages(),
    package_data={'ETHregions2Woredas': ['data.json']},
    description='A package containing code parser and json of regions, zones, and woredas data',
    author='Gashaw Demlew',
    author_email='gashudemman@gmail.com',
    url='https://github.com/gashawdemlew/ETHregions2Woredas',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)