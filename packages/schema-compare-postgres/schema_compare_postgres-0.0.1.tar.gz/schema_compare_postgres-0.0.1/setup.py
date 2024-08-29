from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="schema_compare_postgres",
    version="0.0.1",
    author="Isaque Menezes",
    author_email="isaquesantos1517@gmail.com",
    description="Este pacote Python permite comparar estruturas de bancos de dados PostgresSQL, identificando "
                "diferenças entre tabelas, views, procedures e funções. Ideal para auditorias e sincronizações "
                "entre ambientes de banco de dados.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Isaquemz/schema_compare_postgres.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
