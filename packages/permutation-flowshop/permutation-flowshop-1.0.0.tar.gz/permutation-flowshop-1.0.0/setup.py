from setuptools import setup

with open("README.md", "r") as file:
    read_me = file.read()

setup(
    name='permutation-flowshop',
    version='1.0.0',
    license='MIT License',
    author='Bruno, Raphael',
    packages=['pfsp'],
    long_description=read_me,
    long_description_content_type="text/markdown",
    author_email='bruno.development3@gmail.com',
    keywords='permutation flowshop',
    description=u'Package to facilitate studies about Permutation Flow Shop Scheduling Problem (PFSP)',
    install_requires=['pandas== 2.2.2', 'numpy==2.1', 'plotly==5.24.0'],
)
