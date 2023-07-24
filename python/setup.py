#!/usr/bin/env python3

from setuptools import setup


def get_version():
    with open("debian/changelog", "r", encoding="utf-8") as f:
        return f.readline().split()[1][1:-1]


setup(
    name="",
    version=get_version(),
    description="",
    license="MIT",
    author="",
    author_email="",
    maintainer="Wiren Board Team",
    maintainer_email="info@wirenboard.com",
    url="https://github.com/wirenboard/wb-nm-helper",
    packages=[],
)
