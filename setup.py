"""
Release process:
    1. Update downloadcarr.__version__.__version__
    2. Change download_url below
    3. Commit changes & push
    4. `git tag` the release
    5. Push tags
    6. Change download_url back to master; commit & push
"""
import os.path
from setuptools import setup, find_packages

__here__ = os.path.dirname(os.path.realpath(__file__))

ABOUT = {}
with open(os.path.join(__here__, "downloadcarr", "__version__.py"), "r") as f:
    exec(f.read(), ABOUT)

with open(os.path.join(__here__, "README.rst"), "r") as f:
    README = f.read()

URL_BASE = "{}/tarball".format(ABOUT["__url__"])

setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__description__"],
    long_description=README,
    long_description_content_type="text/x-rst",
    author=ABOUT["__author__"],
    author_email=ABOUT["__author_email__"],
    url=ABOUT["__url__"],
    packages=find_packages(),
    python_requires=">=3.7",
    license=ABOUT["__license__"],
    # Note: change 'master' to the tag name when releasing a new version
    download_url="{}/master".format(URL_BASE),
    #  download_url="{}/{}".format(URL_BASE, ABOUT["__version__"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["sonarr", "radarr"],
)
