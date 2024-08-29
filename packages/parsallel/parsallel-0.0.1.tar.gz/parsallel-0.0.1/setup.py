import setuptools
import subprocess
import os

parsallel_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in parsallel_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = parsallel_version.split("-")
    parsallel_version = v + "+" + i + ".git." + s

assert "-" not in parsallel_version
assert "." in parsallel_version

assert os.path.isfile("parsallel/version.py")
with open("parsallel/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % parsallel_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="parsallel",
    version=parsallel_version,
    author="Rishiraj Acharya",
    author_email="heyrishiraj@gmail.com",
    description="📚 Efficient PDF Parsing in Parallel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rishiraj/parsallel",
    packages=setuptools.find_packages(),
    package_data={"parsallel": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
)