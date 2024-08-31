from setuptools import setup, find_packages

setup(
    name="vinayaga",
    version="0.2.2",
    description="A simple Python package for hypothesis training.",
    author="Arasu",
    author_email="arasu6262@gmail.com",
    license="MIT",
    packages=find_packages(include=['vinayaga', 'vinayaga.*']),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'vinayaga=vinayaga.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
