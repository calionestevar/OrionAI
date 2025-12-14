from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orionai",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="OrionAI - Industry-agnostic AI validation, monitoring, and safety framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/calionestevar/OrionAI",
    py_modules=["orionai"],
    install_requires=[
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "ml": ["transformers>=4.30.0", "torch>=2.0.0"],
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - pure Python!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aicastle=aicastle:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json"],
    },
)
