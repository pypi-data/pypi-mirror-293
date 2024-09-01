from setuptools import setup, find_packages

setup(
    name='fbgrouting',  # Nombre del paquete
    version='0.1',  # Versión inicial
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    include_package_data=True,  # Incluye otros archivos del paquete
    description='fbgrouting - packete de creacion de rutas',  # Descripción breve
    long_description=open('README.md').read(),  # Descripción larga desde README
    long_description_content_type='text/markdown',  # Tipo de contenido del README
    author='Tu Nombre',  # Tu nombre
    author_email='tu.email@example.com',  # Tu correo electrónico
    url='https://github.com/usuariomen/fbgrouting',  # URL de tu repositorio o sitio
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
