import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="shii_study",
  version="1.1.3",
  author="boran",
  author_email="boran@shii.me",
  description="PYPI tutorial package creation written by Boran",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/boranloves/shii",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=['setuptools>=61.0', 'wheel', "korcen>=0.3.13", "json", "logging"],
  python_requires='>=3.8',
)