#!/usr/bin/env python

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages

# setup itself.
setup(
    name = "django-image-sitemaps",
    version = '1.1.0',
    install_requires = ['django>=1.3'],
    packages = find_packages(),
    data_files=[('imagesitemaps/templates', ['imagesitemaps/templates/image_sitemap.xml'])],
    author = "Francois Vantomme",
    author_email = "akarzim@gmail.com",
    description = "Google Image Sitemaps builder for Django.",
    license = "BSD License",
    keywords = "google, django, image, sitemap",
    url = "https://github.com/akarzim/image-sitemaps/",
    #download_url = "https://github.com/akarzim/image-sitemaps/tarball/master",
    include_package_data = True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Internet",
        "Natural Language :: English"
    ],
)

