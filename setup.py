import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metanorm",
    version=os.getenv('METANORM_RELEASE', '0.0.0dev'),
    author="Adrien Perrin, Arash Azamifard",
    author_email="adrien.perrin@nersc.no",
    description="Normalizing tool for Geospatial metadata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nansencenter/metanorm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
)
