from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='semantic-commit',
    version='1.2.0',
    description='scommit: ChatGPT-generated commit messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Globe-Knowledge-Solutions/semantic-commit',
    author='Ivan Yevenko, Brian Machado, Parth Sareen',
    author_email='ivan@globe.engineer, psareen@uwaterloo.ca',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tiktoken',
        'requests',
        'transformers',
    ],
    entry_points={
        'console_scripts': [
            'scommit=scommit:scommit',
        ],
    },
)