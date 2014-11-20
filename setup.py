#! /usr/bin/env python

import codecs
import os
from setuptools import setup

setup(
	name="django-mathfield",
	version="0.1.0",
	description="Write LaTeX in the Django admin and have it rendered to HTML for you.",
	long_description=codecs.open(
		os.path.join(os.path.dirname(__file__), 'README.rst'), 'r', 'utf-8').read(),
	author="Jonathan Goodnow",
	author_email="jon@goodnow.io",
	url="https://github.com/jongoodnow/django-mathfield",
	keywords=["django", "math", "latex", "katex"],
	license="BSD",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: BSD License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.7",
		"Environment :: Web Environment",
		"Framework :: Django",
		"Topic :: Utilities",
	],
	packages=["mathfield"],
	test_suite="tests",
	include_package_data=True,
)