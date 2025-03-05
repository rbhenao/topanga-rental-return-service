from setuptools import setup, find_packages

setup(
    name="topanga_queries",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "reset-db=topanga_queries.scripts.reset_db:initialize_challenge_db",
        ],
    },
)
