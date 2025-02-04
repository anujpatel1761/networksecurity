'''
Thes setup.py file is an essential part of packaging and distributing python packages.
It is used by setup tools to define the configuration of your prohject, 
such as metadata, dependencies and more
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """

    requirement_list:List[str]= []


    try:
        with open('requirements.txt','r') as file:
            # read lines from the file
            lines = file.readlines()
            ## Process each line
            for line in lines:
                requirement = line.strip()
                ## Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("Requirements.txt File Is Not Found")

    return requirement_list


"""
setup(
    name="your-package-name",      # Required - name of your package
    version="0.1.0",              # Required - version of your package
    author="Your Name",           # Optional - author's name
    author_email="your@email.com", # Optional - author's email
    description="Package description", # Optional - short description
    long_description=long_description, # Optional - long description (usually from README)
    packages=find_packages(),     # Required - which packages to include
    install_requires=[            # Optional - package dependencies
        "package1",
        "package2>=1.0.0",
    ],
    python_requires=">=3.6",      # Optional - python version requirement
)

"""

setup(
    name="Networksecurity",
    version="0.0.1",
    author="Anuj Patel",
    author_email="anujpatel1761@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)

#print(get_requirements())