from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="SimpleCapp Calculation Engine",
    url="https://github.com/GustavoRonconi/simplecapp_calculation_engine",
    author="Gustavo A. Ronconi",
    author_email="gustavo.ronconi@simplecapp.com.br",
    version="0.1.0",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # TODO Colocar uma licença fechada aqui
    package_dir={"": "calculation_engine"},
    packages=find_packages(where="calculation_engine"),
    python_requires=">=3.8",
)
