from setuptools import setup, find_packages

setup(
    name="rznpy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1,<3.0.0",
        # Add any other dependencies your project requires
    ],
    author="Your Name",
    author_email="pypi@sarav.xyz",
    description="A client library for interacting with the Rzn Tauri application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/srv1n/rznpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
