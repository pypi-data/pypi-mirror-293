# from setuptools import setup
from distutils.core import setup

# import versioneer

requirements = []

setup(
    name="rdhyee_test",
    version="0.1.5",
    description="a test package ",
    license="MIT",
    author="Raymond Yee",
    author_email="raymond.yee@gmail.com",
    url=None,
    packages=["rdhyee_test"],
    py_modules=["rdhyee_test"],
    install_requires=requirements,
    keywords="rdhyee_test",
    classifiers=[
        # update this
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT",

    ],
)
