from setuptools import setup, find_packages

setup(
    name='eduling',
    version='0.1',
    packages=find_packages(),
    description='Un módulo de enciclopedia y diccionario para Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='tuemail@example.com',
    url='https://github.com/tuusuario/eduling',  # Reemplaza con la URL de tu repositorio
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
