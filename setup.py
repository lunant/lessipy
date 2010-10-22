"""
Lessipy
-------
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Lessipy",
    version="0.0.1",
    license="MIT",
    author="xymz",
    author_email="xym@lunant.net",
    description="LESS python implementation",
    long_description=__doc__,
    packages=["lessipy"],
    platforms="any",
    install_requires=[
        "PIL", "lepl"
    ],
    test_suite="test",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License"
    ]
)

