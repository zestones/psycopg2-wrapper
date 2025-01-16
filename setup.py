from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='psycopg2-wrappers',
    version='1.0.2',  # current_version
    description='psycopg2-wrapper is a wrapper for psycopg2 that makes it easier to use.',
    author='zestones',
    author_email='idrissbenguezzou@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
