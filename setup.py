import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mender-python-client-mendersoftware",
    version="0.0.1",
    license="Apache 2.0",
    author="Mendersoftware",
    author_email="contact@mender.io",
    description="A Python implementation of the Mender client interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mendersoftware/mender-python-client",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    keywords=["mender", "OTA", "updater"],
    install_requires=["cryptography", "requests", "argparse"],
    entry_points={"console_scripts": ["mender=mender:main"]},
    python_requires=">=3.6",
    zip_safe=False,
    include_package_data=True,
)
