import shutil
from setuptools import setup, find_packages


shutil.rmtree("build", ignore_errors=True,)
shutil.rmtree("clickhttp.egg-info", ignore_errors=True,)

with open(file="requirements.txt", mode="r",) as f:
    requirements = f.read().splitlines()

with open(file="README.md", mode="r", encoding="utf-8",) as f:
    long_description = f.read()

setup(name="clickhttp",
      version="0.0.6",
      packages=find_packages(),
      install_requires=requirements,
      author="0xMihalich",
      author_email="bayanmobile87@gmail.com",
      description="Работа с БД Clickhouse по HTTP-протоколу",
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False,)
