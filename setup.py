#!/usr/bin/env python

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages

# setup itself.
setup(
    name = "Django image sitemaps",
    version = '1.0 alpha',
    install_requires = ['django>=1.3'],
    packages = find_packages(),
    author = "Francois Vantomme",
    author_email = "akarzim@gmail.com",
    description = "Google Image Sitemaps builder for Django.",
    license = "LICENSE",
    keywords = "google, django, image, sitemap",
    url = "https://github.org/akarzim/django-image-sitemaps/",
    include_package_data = True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)

