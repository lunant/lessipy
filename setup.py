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
    author_email="",
    description="",
    long_description=__doc__,
    packages=["lessipy"],
    platforms="any",
    install_requires=[
        "PIL"
    ],
    test_suite="test",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console"
    ]
)

