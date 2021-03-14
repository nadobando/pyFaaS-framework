from setuptools import setup

# with open("src/faas_framework/__init__.py", encoding="utf8") as f:
#     version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="pyfaas-framework",
    version="1.0.1",
    install_requires=[
        "pydantic",
        "pydantic[email]",
        "typing-extensions; python_version < '3.8'",
        "aws-lambda-powertools",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-mock" "pytest-lazy-fixture"
            # "tox",
            # "sphinx",
            # "pallets-sphinx-themes",
            # "sphinxcontrib-log-cabinet",
            # "sphinx-ipipessues",
        ],
    },
)
