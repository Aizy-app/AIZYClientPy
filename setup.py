from setuptools import setup, find_packages
import os
import re

def get_version():
    init_file = os.path.join("aizypy", "__init__.py")
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Cannot find version string")

with open("PYPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aizypy",
    version=get_version(),
    author="Aizy Team",
    author_email="contact@aizy.app",
    description="A Python framework for creating and testing trading bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aizy-app/AIZYClientPy",
    packages=["aizypy"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "websockets>=10.0",
        "aiohttp>=3.8.0",
        "python-dateutil>=2.8.2",
        "pytz>=2021.3",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
        ],
    }
)
