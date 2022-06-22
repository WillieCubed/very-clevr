from setuptools import setup

setup(
    name="very-clevr",
    version="0.1.0",
    packages=["very_clevr"],
    # ...
    entry_points={
        "console_scripts": [
            "vc=very_clevr.utils:run_cli",
        ]
    },
)
