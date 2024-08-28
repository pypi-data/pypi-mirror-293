from setuptools import setup, find_packages

setup(
    name="mtune",
    version="1.0",
    author="Gori Sankar Borah, Hillul Chutia ",
    author_email="gorishankarbora45@gmail.com, hillulchutia@gmail.com",
    description="Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)
