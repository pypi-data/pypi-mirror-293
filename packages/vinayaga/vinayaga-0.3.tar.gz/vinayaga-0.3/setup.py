from setuptools import setup, find_packages

setup(
    name="vinayaga",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',  # Main dependencies
        'numpy',
    ],
    extras_require={
        'excel': ['openpyxl'],  # Optional dependencies for Excel support
    },
    package_data={
        'vinayaga': ['data.csv'],  # Include data.csv file in the package
    },
    description="A simple package for hypothesis generation using a custom train function",
    long_description=open('README.md').read(),  # Add a long description from README.md
    long_description_content_type='text/markdown',  # Format of the long description
    author="arasu",
    author_email="arasum6262@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "vinayaga-cli = vinayaga.cli:main",  # Define the CLI command
        ],
    },
)
