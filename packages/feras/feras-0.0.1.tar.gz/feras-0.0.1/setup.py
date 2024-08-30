from setuptools import setup, find_packages

setup(
    name="feras",
    version="0.0.1",
    author="fares7816",
    author_email="fares.djelili@outlook.fr",
    url="",
    description="Un package pour créer des réseaux de neurones denses",
    packages=find_packages(),
    readme="README.md",
    install_requires=["numpy >= 1.23.3"],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
