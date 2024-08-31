from setuptools import setup, find_packages

setup(
    name="chippapi",
    version="1.0.2",
    description="A module for interacting with the Chipp API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="skilledkitten",
    author_email="me@skilledkitten.dev",
    url="https://github.com/skilledkitten/chippapi",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)