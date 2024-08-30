from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="currencies_lib",
    version="1.0.3",
    description="A currency formatter for many currencies",
    packages=find_packages(where="."),
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamtwobe/currencies_lib",
    author="iamtwobe",
    author_email="contato.iamtwobe@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[""],
    extras_require={
    },
    python_requires=">=3.10",
)