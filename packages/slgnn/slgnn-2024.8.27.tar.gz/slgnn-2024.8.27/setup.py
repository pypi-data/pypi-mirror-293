"""SLGNN"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slgnn",
    version="2024.8.27",
    author="Kamal Choudhary",
    author_email="writetokamal.1989@gmail.com",
    description="slgnn",
    install_requires=[
        "numpy>=1.19.5,<2.0.0",
        "scipy>=1.6.1",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepmaterials/slgnn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
