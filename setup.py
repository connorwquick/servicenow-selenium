from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='servicenow-selenium',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    python_requires='>=3.6',
    author='Seamless Migration',
    description='A simple selenium wrapper for ServiceNow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/connorwquick/servicenow-selenium',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

