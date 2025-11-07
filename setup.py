from setuptools import setup, find_packages

setup(
    name="Quickshop_ETL",
    version="0.1.0",
    description="ETL pipeline for Quickshop",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "sqlalchemy",
        "pydantic",
    ],
)