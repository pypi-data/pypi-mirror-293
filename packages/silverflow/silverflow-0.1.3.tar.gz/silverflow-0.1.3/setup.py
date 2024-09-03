from setuptools import setup, find_packages


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]


setup(
    name="silverflow",
    version="0.1.3",
    author="Silvestro",
    author_email="hello@silverstream.ai",
    description="SilverRiver SDK for advanced automation and AI-driven tasks",
    long_description=open("src/silverriver/README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/manuel-delverme/silver_river",
    # packages=find_packages(where="src/silverriver"),
    # package_dir={"": "src/silverriver"},
    package_dir={"": "src"},  # Tells setuptools to look in src/ for packages
    packages=find_packages(where="src", include=["silverriver*"]),  # Only include the silverriver package
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=parse_requirements('src/silverriver/requirements.txt'),
)
