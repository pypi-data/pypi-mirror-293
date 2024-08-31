from setuptools import setup, find_packages

setup(
    name="holosen-pass-generator",
    version="0.1.0",
    author="Python Knight",
    author_email="holosenpythonknight@gmail.com",
    description="A simple Python library to generate 3 type of password",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/badrnezhad/password-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
