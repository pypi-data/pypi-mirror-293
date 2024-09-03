from setuptools import setup, find_packages

setup(
    name='enjoysport',
    version='0.3.3',
    author='Arasu',
    author_email='arasum6262@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
    ],
)
