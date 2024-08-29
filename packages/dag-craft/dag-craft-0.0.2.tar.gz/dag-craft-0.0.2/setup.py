from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="dag-craft",
    version="0.0.2",
    url="https://github.com/MurilloSSJ/airflow-dag-factory",
    license="MIT License",
    author="Murillo Jacob",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="murillostore@gmail.com",
    keywords="Airflow, DAG, Factory",
    description="Dag Factory para o Airflow",
    packages=["dag_craft"],
    install_requires=["apache-airflow"],
)
