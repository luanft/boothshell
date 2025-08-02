"""Setup script for the Photoserver project."""
from setuptools import setup, find_packages

setup(
    name="photoserver",
    version="1.0.9",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.13",
        "uvicorn==0.34.3",
        "dotenv==0.9.9",
        "python-dotenv==1.1.1"
    ],
    author="luanft",
    author_email="xcrossworker@gmail.com",
    description="Booth shell for photoserver.",
    long_description=open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luanft/boothshell",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Thay đổi nếu bạn dùng license khác
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "boothshellservice = main:main",
            # "photoserver_com = photoserver.service:main"
        ]
    }
)