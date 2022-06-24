from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="very-clevr",
    version="0.1.0",
    packages=["very_clevr", "much_clevr"],
    description="",
    long_description=long_description,
    author="Willie Chalmers III",
    author_email="willie@williecubed.me",
    url="https://williecubed.github.io/very-clevr",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "vc=very_clevr.utils:run_cli",
        ]
    },
)
