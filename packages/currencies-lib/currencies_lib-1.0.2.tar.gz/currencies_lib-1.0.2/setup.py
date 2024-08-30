from setuptools import find_packages, setup


setup(
    name="currencies_lib",
    version="1.0.2",
    description="A currency formatter for many currencies",
    packages=find_packages(where="."),
    long_description="A currency formatter library with more specific formats for every currency",
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