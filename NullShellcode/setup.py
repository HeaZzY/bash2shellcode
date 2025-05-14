from setuptools import setup, find_packages

setup(
    name="shellgen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "keystone-engine>=0.9.2",
        "capstone>=4.0.2",
    ],
    entry_points={
        "console_scripts": [
            "shellgen=shellgen.cli:main",
        ],
    },
    author="Your Name",
    description="Un générateur de shellcode optimisé et obfusqué",
    keywords="shellcode, security, assembly, exploitation",
    python_requires=">=3.7",
) 