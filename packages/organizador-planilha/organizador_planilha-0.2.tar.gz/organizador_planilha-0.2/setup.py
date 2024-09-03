from setuptools import setup, find_packages

setup(
    name="organizador_planilha",  # Nome do pacote
    version="0.2",  # Versão inicial
    author="Seu Nome",
    author_email="seu_email@example.com",
    description="Um pacote simples para buscar e organizar planilhas em um banco MYSQL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MoisesAlves2023/organizador_planilha",  # Atualize com a URL do repositório
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'pandas',
        'sqlalchemy',
        'openpyxl',
        'pymysql',
        'tkinter',
    ],
)
