from setuptools import setup, find_namespace_packages

setup(
    name='tuneout',
    version='0.0.1',
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True
)
