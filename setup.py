from setuptools import setup, find_packages

setup(
    name='scommit',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tiktoken',
    ],
    entry_points={
        'console_scripts': [
            'scommit=scommit:scommit',
        ],
    },
)