from setuptools import setup, find_packages

setup(
    name='common_stats',
    version='0.0.1',
    description='A simple library for basic statistical calculations',
    author='Paras Arora',
    author_email='parasaroraee@gmail.com',
    packages=find_packages(),
    install_requires=[
        "pytest"
    ],
    license='MIT',
    python_requires='>=3.7',
)