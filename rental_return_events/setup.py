import os
from setuptools import setup, find_packages

# Dynamically get absolute path to topanga_queries
topanga_queries_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../topanga_queries"))

setup(
    name="rental_return_events",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        f"topanga_queries @ file://{topanga_queries_path}",
        "tabulate==0.9.0",
        "iniconfig==2.0.0",
        "packaging==24.2",
        "pluggy==1.5.0",
        "pytest==8.3.5"
    ],
    entry_points={
        "console_scripts": [
            "process-return=rental_return_events.scripts.process_return:main",
        ],
    },
)