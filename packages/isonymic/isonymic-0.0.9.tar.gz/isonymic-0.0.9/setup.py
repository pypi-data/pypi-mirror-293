from setuptools import find_packages, setup

with open(
    "/home/lmorales/work/pipelines/package_surnames/isonymic_package/app/README.md", "r"
) as f:
    long_description = f.read()

setup(
    name="isonymic",
    version="0.0.9",
    description="A simple Python package for isonymy studies from population surnames",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoMorales/isonymic-package",
    author="LeoMorales",
    author_email="moralesleonardo.rw@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.6",
)
