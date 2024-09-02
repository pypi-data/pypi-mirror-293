from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as reqs:
    requirements_list = [line.strip() for line in reqs if line.strip()]

setup(
    name="ethina",
    version="0.1-alpha",
    author="Kshitij S. Tyagi",
    author_email="hello@brahmai.in",
    description="A unified interface for interacting with various Language Model (LLM) providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kstyagi23/Ethina",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=requirements_list,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "flake8",
            "black",
        ],
    },
    include_package_data=True,
    package_data={"": ["*.txt", "*.md"]},
)
