from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="prime-visualizer",
    version="1.0.0",
    author="Johan",
    author_email="your.email@example.com",
    description="Visualize prime numbers in a color-coded grid",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/prime-visualizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "prime_visualizer": ["config.yaml"],
    },
    entry_points={
        "console_scripts": [
            "prime-visualizer=prime_visualizer.run:main",
        ],
    },
)