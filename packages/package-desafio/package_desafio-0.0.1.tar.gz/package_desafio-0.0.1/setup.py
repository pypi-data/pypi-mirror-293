from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()  # Corrigido o operador de atribuição '='

with open("requirements.txt") as f:
    requirements = f.read().splitlines()  # Corrigido o operador de atribuição '='

setup(
    name="package_desafio",  # Corrigido o operador de atribuição '=' e colocado entre aspas
    version="0.0.1",  # Corrigido o operador de atribuição '=' e colocado entre aspas
    author="Leonardo Durante",  # Corrigido o operador de atribuição '=' e colocado entre aspas
    author_email="leo.durante_@hotmail.com",  # Corrigido o operador de atribuição '=' e colocado entre aspas
    description="My short description",  # Corrigido o operador de atribuição '='
    long_description=page_description,  # Corrigido o operador de atribuição '='
    long_description_content_type="text/markdown",  # Corrigido o operador de atribuição '='
    url="https://github.com/LeeoDurante/image-processing-package",  # Corrigido o operador de atribuição '=' e colocado entre aspas
    packages=find_packages(),  # Corrigido para 'find_packages' sem espaço e entre parênteses
    install_requires=requirements,  # Corrigido para 'requirements'
    python_requires=">=3.8",  # Corrigido para '>=3.8' e colocado entre aspas
)
