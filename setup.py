#!/usr/bin/env python

from setuptools import find_packages, setup


requirements = open("requirements.txt").readlines()

# setup itself.
setup(
    name="django-image-sitemaps",
    version="2.0.0",
    install_requires=requirements,
    packages=find_packages(),
    author="Francois Vantomme",
    author_email="akarzim@gmail.com",
    description="Google Image Sitemaps builder for Django.",
    license="BSD License",
    keywords="google, django, image, sitemap",
    url="https://github.com/akarzim/image-sitemaps/",
    # download_url = "https://github.com/akarzim/image-sitemaps/tarball/master",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Internet",
        "Natural Language :: English",
    ],
)
