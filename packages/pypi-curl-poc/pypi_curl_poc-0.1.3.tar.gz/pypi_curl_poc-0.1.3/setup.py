from setuptools import setup, find_packages

setup(
    name="pypi-curl-poc",
    version="0.1.3",
    description="A simple imitation of the curl command in Python",
    author="Jorge Llanos",
    author_email="llanosjorge1991@hotmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
