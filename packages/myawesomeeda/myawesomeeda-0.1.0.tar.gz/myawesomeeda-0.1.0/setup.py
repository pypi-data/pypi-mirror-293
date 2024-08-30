from setuptools import setup, find_packages

setup(
    name="myawesomeeda",
    version="0.1.0",
    description="A Python package for awesome EDA",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Ilia Popov",
    author_email="iljapopov17@gmail.com",
    url="https://github.com/iliapopov17/MyAwesomeEDA",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
