from setuptools import setup
import os

HYPHEN_E_DOT = "-e."
DESCRIPTION = "A simple helloworld package."
LONG_DESCRIPTION = """ A simple helloworld package to test package deployment on pypi."""

def get_requirements_as_list(requirements_filepath: str = "requirements.txt"):
    # requirements_filepath = os.path.abspath(requirements_filepath)
    # with open(requirements_filepath, 'r') as reqs:
    #     requirements = reqs.readlines()

    # requirements = remove_hyphen_e_from_requirements(requirements)
    # return requirements
    return []

def remove_hyphen_e_from_requirements(requirements: list):
    try:
        index = requirements.index(HYPHEN_E_DOT)
        requirements[index] = ""
    except ValueError:
        pass

    return requirements


setup(
    name="helloworld_by_shaukat",
    version="0.0.1",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Shaukat Ali Khan",
    author_email="youngdevelopersk@gmail.com",
    packages = get_requirements_as_list(),
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
)