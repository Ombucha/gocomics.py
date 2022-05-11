from pathlib import Path

from setuptools import setup

HERE = Path(__file__).resolve().parent
README = (HERE / "README.rst").read_text()

setup(
    name = "gocomics.py",
    version = "1.0.0",
    description = "Fetch comics from GoComics.",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Pysics/gocomics.py",
    author = "Omkaar",
    author_email = "omkaar.nerurkar@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>= 3.8.0',
    packages = ["gocomics"],
    include_package_data = True,
    install_requires = ["beautifulsoup4"],
)
