# setup.py

from setuptools import setup, find_packages

setup(
    name="uml-generator",
    version="4.1.4",
    author="SIIR3X",
    author_email="siir3xs@gmail.com",
    description="A tool to generate UML diagrams from project files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SIIR3X/python-uml-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "plantuml==0.3.0",
    ],
    entry_points={
        'console_scripts': [
            'uml-generator=uml_generator.main:generate_uml',
        ],
    },
)
