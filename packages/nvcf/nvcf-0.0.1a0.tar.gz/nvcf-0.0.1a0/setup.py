from setuptools import setup, find_packages

setup(
    name="nvcf",
    version="0.0.1-alpha",
    author="t",
    python_requires=">=3.6",
    install_requires=[
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.3",
            "flake8>=3.9.0",
        ],
    },
)
