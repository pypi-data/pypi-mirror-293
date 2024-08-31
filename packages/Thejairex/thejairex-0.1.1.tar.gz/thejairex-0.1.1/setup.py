from setuptools import setup, find_packages

setup(
    name = "Thejairex",
    version= "0.1.1",
    description= "My personal package",
    author = "Thejaiex",
    author_email= "yairjesus777@gmail.com",
    packages= ["Thejairex"],
    install_requires = [
        'fake_useragent',
        'requests',
        ],
    classifiers= [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',

    ],
    python_requires= '>=3.6' 
)