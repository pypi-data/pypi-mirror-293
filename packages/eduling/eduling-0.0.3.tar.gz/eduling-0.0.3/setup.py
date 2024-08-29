from setuptools import setup, find_packages

setup(
    name='eduling',
    version='0.0.3',
    packages=find_packages(),
    description='Un módulo de enciclopedia y diccionario para las funciones de Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lyonnelv20',
    author_email='vidalnelson112@gmail.com',
    url='https://gitlab.com/vidalnelson112/eduling',  # Reemplaza con la URL de tu repositorio
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
