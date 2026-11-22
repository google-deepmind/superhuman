"""Setup configuration for imobench package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")
else:
    long_description = "Python library for loading and working with IMO Bench datasets"

setup(
    name="imobench",
    version="0.1.0",
    author="IMO Bench Contributors",
    author_email="",
    description="Python library for loading and working with IMO Bench mathematical reasoning benchmarks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/google-deepmind/superhuman",
    project_urls={
        "Bug Tracker": "https://github.com/google-deepmind/superhuman/issues",
        "Documentation": "https://imobench.github.io",
        "Source Code": "https://github.com/google-deepmind/superhuman",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        # No external dependencies required - uses only stdlib
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ],
        "pandas": [
            "pandas>=1.5.0",
        ],
    },
    keywords=[
        "mathematics",
        "reasoning",
        "benchmark",
        "imo",
        "olympiad",
        "ai",
        "machine-learning",
        "evaluation",
    ],
)
