from setuptools import setup

setup(
    name="winner",
    version="0.1",
    py_modules=["winner"],
    entry_points={
        "console_scripts": [
            "winner=winner:main",
        ],
    },
    install_requires=[
        "pymongo",
        "python-dotenv",
    ],
)
