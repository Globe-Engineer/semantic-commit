from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='semantic-commit',
    version='0.1',
    description='scommit: ChatGPT-generated commit messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Globe-Knowledge-Solutions/semantic-commit',
    author='Ivan Yevenko',
    author_email='ivan@globe.engineer',
    license='MIT',
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