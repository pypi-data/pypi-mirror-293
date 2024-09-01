from setuptools import setup, find_packages

description = "pwgv (password generation and verification) модуль который состоит из инструкций генераций паролей, проверки и записи"
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='Pwgv',
    version='1.1',
    packages=find_packages(),
    author='G0ga1',
    author_email='andre.web16@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/G0ga1/percent_password',
    python_requires='>=3.12',
)