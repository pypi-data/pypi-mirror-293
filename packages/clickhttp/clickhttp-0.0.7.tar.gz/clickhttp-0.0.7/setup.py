import shutil
from setuptools import setup, find_packages
import pathlib
import pkg_resources


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# parse_requirements() returns generator of pip.req.InstallRequirement objects
# install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# reqs = [str(ir.req) for ir in install_reqs]


shutil.rmtree("build", ignore_errors=True,)
shutil.rmtree("clickhttp.egg-info", ignore_errors=True,)

# with open(file="requirements.txt", mode="r",) as f:
#     requirements = f.read().splitlines()

with open(file="README.md", mode="r", encoding="utf-8",) as f:
    long_description = f.read()

setup(name="clickhttp",
      version="0.0.7",
      packages=find_packages(),
      install_requires=install_requires,
      author="0xMihalich",
      author_email="bayanmobile87@gmail.com",
      description="Работа с БД Clickhouse по HTTP-протоколу",
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False,)
