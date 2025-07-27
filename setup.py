from setuptools import setup, find_packages

setup(
    name="pycba",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "matplotlib<3.8.0",
        "streamlit",
        "plotly",
        "python-dateutil",
        "pyparsing",
        "cycler",
        "kiwisolver",
        "pillow",
        "packaging",
        "six"
    ],
    python_requires=">=3.7,<3.12",
)
