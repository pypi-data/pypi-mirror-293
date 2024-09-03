from setuptools import setup, find_packages

setup(
    name="mandr",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here
        "mandr"
    ],
    author="Camille Troillard",
    author_email="cam@probabl.ai",
    description="All elements eventually decay to Pb...",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/probabl-ai/mandr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
