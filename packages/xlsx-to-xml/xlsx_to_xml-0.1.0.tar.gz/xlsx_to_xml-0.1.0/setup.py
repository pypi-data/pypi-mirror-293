from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="xlsx_to_xml",
    version="0.1.0",
    rust_extensions=[RustExtension("xlsx_to_xml.rust_tool")],
    packages=["xlsx_to_xml"],
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=[
        "setuptools>=42",
        "setuptools-rust>=0.11",
        "wheel",
    ],
)
