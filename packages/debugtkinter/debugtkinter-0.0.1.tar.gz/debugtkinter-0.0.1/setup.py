from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = "A simple debugger for tkinter."
LONG_DESCRIPTION = "A package that allows you to debug tkinter applications."

setup(
    name="debugtkinter",
    version=VERSION,
    author="Berk Efe",
    author_email="berkefekeskin@gmail.com",
    description="A simple debugger for tkinter.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tkinter', 'debugger', 'debugging', 'debug', 'tkinter debugger'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    entry_points={
        "console_scripts": [
            "debugtkinter = debugtkinter.__main__:funny_addition",
        ],
    },
    
    url="https://github.com/berk-efe/debugtkinter",
    python_requires='>=3.6',
)
