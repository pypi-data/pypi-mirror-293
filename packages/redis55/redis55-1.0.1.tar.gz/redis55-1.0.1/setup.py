#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="redis55",
    description="redis55 is forked from redis 5.0.0, so you can use redis55 and any version redis in one python env",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["Redis", "key-value store", "database"],
    license="MIT",
    version="1.0.1",
    packages=find_packages(
        include=[
            "redis55",
            "redis55._parsers",
            "redis55.asyncio",
            "redis55.commands",
            "redis55.commands.bf",
            "redis55.commands.json",
            "redis55.commands.search",
            "redis55.commands.timeseries",
            "redis55.commands.graph",
            "redis55.parsers",
        ]
    ),
    package_data={"redis55": ["py.typed"]},
    include_package_data=True,
    # url="https://github.com/ydf0509/redis55",
    url="",
    project_urls={
        # "Documentation": "https://redis.readthedocs.io/en/latest/",
        # "Changes": "https://github.com/redis/redis-py/releases",
        # "Code": "https://github.com/ydf0509/redis55",
        # "Issue tracker": "https://github.com/redis/redis-py/issues",
    },
    author="Redis Inc.",
    author_email="",
    python_requires=">=3.7",
    install_requires=[
        'importlib-metadata >= 1.0; python_version < "3.8"',
        'typing-extensions; python_version<"3.8"',

    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    extras_require={
        "hiredis": ["hiredis>=1.0.0"],
        "ocsp": ["cryptography>=36.0.1", "pyopenssl==20.0.1", "requests>=2.26.0"],
    },
)
