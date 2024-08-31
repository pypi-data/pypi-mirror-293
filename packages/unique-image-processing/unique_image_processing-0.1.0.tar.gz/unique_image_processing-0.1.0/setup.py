from setuptools import setup, find_packages

setup(
    name="unique_image_processing",
    version="0.1.0",
    description="Um pacote para processamento de imagens",
    author="Fabiano Navarro",
    author_email="nav.info.suporte@gmail.com",
    license="MIT",
    packages=find_packages(include=["image_processing", "image_processing.processing", "image_processing.utils"]),
    include_package_data=True,  # Inclui arquivos de dados
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
