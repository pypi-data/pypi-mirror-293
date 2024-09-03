from setuptools import setup, find_packages

setup(
    name='enjoysport',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'enjoysport=enjoysport.enjoysport:main'
        ],
    },
    package_data={
        'enjoysport': ['enjoysport.csv'],  # Include the CSV file
    },
)
