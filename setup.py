from setuptools import setup, find_packages


description_files = ["README.rst", "AUTHORS.rst", "CHANGELOG.rst"]

setup(
    name="django-formfactory",
    description="Dynamic django form builder.",
    long_description="".join([open(f, "r").read() for f in description_files]),
    version="0.2.3",
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://github.com/praekelt/django-formfactory",
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        "django>1.11,<3.0",
        "django-formtools>=2.1",
        "django-simplemde>=0.1.2",
        "markdown",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 1.11",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
    include_package_data=True
)
