from setuptools import setup, find_packages

setup(
    name="rayshnakht",
    version="0.1.0",
    author="Patnutsh",
    author_email="patnutsh@proton.me",
    description="A custom hashing algorithm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rayshnakht",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)