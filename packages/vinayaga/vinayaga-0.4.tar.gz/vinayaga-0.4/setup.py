from setuptools import setup, find_packages

setup(
    name="vinayaga",
    version="0.4",  # Increment the version number
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
    ],
    package_data={
        'vinayaga': ['data.csv'],
    },
    description="A simple package for hypothesis generation using a custom train function",
    author="arasu",
    author_email="arasum6262@gmail.com",
)
