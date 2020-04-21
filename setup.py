import re

from setuptools import setup

# with open("src/flask/__init__.py", encoding="utf8") as f:
#     version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="lamb-frame",
    version="1.0.0",
    install_requires=[
        "python-dotenv",
        "pydantic",
        "pydantic[email]",
        "typing-extensions; python_version < '3.8'",
        "aws-lambda-powertools"

        # "Werkzeug>=0.15",
        # "Jinja2>=2.10.1",
        # "itsdangerous>=0.24",
        # "click>=5.1",
    ],
    
    extras_require={
        "dev": [
            "pytest",
            "coverage",
            # "tox",
            # "sphinx",
            # "pallets-sphinx-themes",
            # "sphinxcontrib-log-cabinet",
            # "sphinx-ipipessues",
        ],
    },
    # dependency_links=[
    #     "file:///Users/Nadir.Albajari/Documents/Work/aws-lambda-powertools-python/dist/aws_lambda_powertools-1.10.1/dist/nb_aws_lambda_powertools-1.10.1-py3.8.egg#egg=nb-aws-lambda-powertools-1.10.1"
    # ]
)
