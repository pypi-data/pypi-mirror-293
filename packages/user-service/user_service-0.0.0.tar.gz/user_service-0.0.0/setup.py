from setuptools import setup, find_namespace_packages, find_packages
import re
import pathlib
import pkg_resources

requirements = None
with pathlib.Path('requirements.txt').open() as requirements_txt:
    requirements = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]
# Retrieve package list
PACKAGES = find_packages()
#(find_namespace_packages(include=["src*"]))

# Add extra virtual shortened package for each of namespace_pkgs
namespace_pkgs = ["users"]
exclusions = r"|".join(
    [r"\." + item + r"\.(?=" + item + r".)" for item in namespace_pkgs]
)
PACKAGE_DIR = {}
for package in PACKAGES:
    sub_tmp = re.sub(exclusions, ".", package)
    if sub_tmp is not package:
        PACKAGE_DIR[sub_tmp] = package.replace(".", "/")
PACKAGES.extend(PACKAGE_DIR.keys())

# Run python setup
setup(
    name="user_service",
    version="0.0.0",
    description=(
        "A parent python package."
    ),
    install_requires=requirements,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
)