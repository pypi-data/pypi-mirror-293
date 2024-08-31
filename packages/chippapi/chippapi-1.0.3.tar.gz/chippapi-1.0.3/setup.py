from setuptools import setup, find_packages

setup(
    name="chippapi",
    version="1.0.3",
    description="This is a simple python wrapper for [Chipp](https://chipp.ai/).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="skilledkitten",
    author_email="me@skilledkitten.dev",
    url="https://github.com/skilledkitten/chippapi",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)
