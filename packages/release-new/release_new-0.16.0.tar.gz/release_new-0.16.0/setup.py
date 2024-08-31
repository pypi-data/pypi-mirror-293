#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from setuptools import find_packages, setup

pkginfo = Path(__file__).parent / "__pkginfo__.py"
__pkginfo__ = {}
with pkginfo.open() as f:
    exec(f.read(), __pkginfo__)

distname = "release-new"
version = __pkginfo__["version"]
license = "LGPL"
description = "logilab's tool to make easy releases on our forge with mercurial"

with open("./README.md", "r") as f:
    long_description = f.read()

author = "Logilab"
author_email = "contact@logilab.fr"
requires = {
    "redbaron": ">=0.9.2,<0.10",
    "jinja2": None,
    "mercurial": ">=6.5.1,<7",
    "tomlkit": None,
    "semver": ">=3.0.2,<4.0.0",
}

install_requires = ["{0} {1}".format(d, v or "").strip() for d, v in requires.items()]

setup(
    name=distname,
    version=version,
    license=license,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url="https://forge.extranet.logilab.fr/open-source/release-new",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={"console_scripts": ["release-new = release_new.main:main"]},
)
