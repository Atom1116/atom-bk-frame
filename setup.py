import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atom_bk_frame",
    version="0.0.1",
    author="Atom1116",
    author_email="atom1116@example.com",
    description="a web framework for small backends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Atom1116/atom_bk_frame",
    project_urls={
        "Bug Tracker": "https://github.com/Atom1116/atom_bk_frame",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "atom_bk_frame"},
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)