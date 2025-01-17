from setuptools import setup, find_packages

setup(
    name="aizypy",
    version="0.2.0",
    author="Aizy Team",
    author_email="contact@aizy.app",
    description="A Python framework for creating and testing trading bots",
    url="https://github.com/aizy-app/AIZYClientPy",
    packages=find_packages(),
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
