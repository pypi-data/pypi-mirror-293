from setuptools import find_packages, setup

setup(
    name="KAFYTraj",
    packages=find_packages(include=["KAFY", "KAFY.*"]),
    version="0.1.1",
    description="This library includes an extensible system for building various trajectory operations.",
    author="Youssef Hussein",
    # install_requires --> should be limited to the list of packages that are absolutely needed.
    # Also note that you do not need to list packages that are part of the standard Python library.
)
