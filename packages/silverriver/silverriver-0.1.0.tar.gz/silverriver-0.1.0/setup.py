from setuptools import setup, find_packages

setup(
    name="silverriver",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Your Name",
    author_email="your.email@example.com",
    description="SilverRiver SDK for advanced automation and AI-driven tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manuel-delverme/silver_river",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx",
        "pydantic",
        "playwright",
        "slack_sdk",
        "tabulate",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "mypy",
        ],
    },
)
