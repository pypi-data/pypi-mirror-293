from setuptools import setup, find_packages

setup(
    name="dconvert",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "et-xmlfile",
        "lxml",
        "numpy",
        "openpyxl",
        "pandas",
        "python-dateutil",
        "pytz",
        "six",
        "tzdata"
    ],
    entry_points={
        'console_scripts': [
            'dconvert=dconvert.__main__:main',  # Points to main() in __main__.py inside the dconvert package
        ],
    },
    author="Aaron Mathis",
    description="A tool for converting data formats.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/aaronlmathis/dconvert",  # Replace with your project's URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPL-3.0",
    python_requires='>=3.6',
)
