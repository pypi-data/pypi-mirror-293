from setuptools import setup, find_packages

setup(
    name="log_abstractor",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "structlog>=24.4.0", "anonypy>=0.1.7",
    ],
    description="A configurable logging abstraction using structlog.",
    author="Dipanjan Mazumder",
    author_email="javahub@yahoo.com",
    url="https://github.com/SMART2016/logger",  # Optional: Link to your project repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
