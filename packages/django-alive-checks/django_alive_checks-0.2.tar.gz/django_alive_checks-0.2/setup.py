from setuptools import find_packages, setup

setup(
    name="django-alive-checks",
    version="0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "django-alive",
    ],
    extras_require={
        "elasticsearch": ["elasticsearch>=7.0.0"],
    },
    description="Additional health checks for django-alive",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/PetrDlouhy/django-alive-checks",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
