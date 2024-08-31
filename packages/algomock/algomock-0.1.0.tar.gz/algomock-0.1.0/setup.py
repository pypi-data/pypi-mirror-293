from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="algomock",
	version="0.1.0",
	author="getCurrentThread",
	author_email="wak8835@gmail.com",
	description="A flexible input generator for algorithm testing",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/getCurrentThread/algomock",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
