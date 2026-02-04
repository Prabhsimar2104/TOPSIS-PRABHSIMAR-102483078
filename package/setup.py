from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for PyPI description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="Topsis-Prabhsimar-102483078",
    version="1.0.5",  # 🔧 bumped version
    author="Prabhsimar Singh",
    author_email="pbatra_be23@thapar.edu",  # 🔧 real email
    description="A Python package for TOPSIS multi-criteria decision making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",  # 🔧 explicitly added
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    python_requires=">=3.6",  # ✅ keep as-is
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_prabhsimar_102483078.topsis:topsis"
        ]
    },
)