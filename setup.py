from setuptools import setup, find_packages

setup(
    name="AizyPy",
    version="0.3",
    description="Wrapper around Aizy bot methods for local testing and development.",
    author="Aizy Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
        "asyncio>=3.4.3",
        "typing-extensions>=4.7.1",
    ],
    python_requires=">=3.7",
)
