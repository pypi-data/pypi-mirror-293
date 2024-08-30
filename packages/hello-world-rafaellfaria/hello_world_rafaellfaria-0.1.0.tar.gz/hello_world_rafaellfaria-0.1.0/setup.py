from setuptools import setup, find_packages

setup(
    name="hello_world_rafaellfaria",
    version="0.1.0",
    author="Rafael",
    author_email="joaorafaelfaria@gmail.com",
    description="A simple hello world package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
