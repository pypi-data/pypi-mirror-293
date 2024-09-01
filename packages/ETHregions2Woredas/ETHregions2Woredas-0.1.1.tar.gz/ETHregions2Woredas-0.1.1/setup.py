from setuptools import setup, find_packages

setup(
    name='ETHregions2Woredas',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ETHregions2Woredas': ['data.json'],
    },
    install_requires=[
        # Add your dependencies here
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ETHregions2Woredas',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)