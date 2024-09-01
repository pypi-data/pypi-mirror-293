from setuptools import setup, find_packages

setup(
    name="recursive_rebase",
    author="Farzan Hashmi",
    author_email="farzan.hashmi@berkeley.edu",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "recursive-rebase = recursive_rebase.main:main",
        ],
    },
)
