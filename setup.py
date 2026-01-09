from setuptools import setup, find_packages

setup(
    name="recondorker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "beautifulsoup4",
        "click",
        "rich",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "recondorker=recondorker.cli:main",
        ],
    },
)
