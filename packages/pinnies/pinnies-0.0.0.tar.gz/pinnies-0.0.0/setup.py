from setuptools import setup, find_packages

setup(
    name="pinnies",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[],
    description="A Physics-Informed Neural Network Framework for Solving Integral Equations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Alireza Afzal Aghaei",
    author_email="alirezaafzalaghaei@gmail.com",
    license="MIT",
)
