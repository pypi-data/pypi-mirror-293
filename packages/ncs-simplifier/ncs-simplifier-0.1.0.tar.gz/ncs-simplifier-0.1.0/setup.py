from setuptools import setup, find_packages

setup(
    name='ncs-simplifier',
    version='0.1.0',
    description='Simplifica a interação com dispositivos de rede utilizando Cisco NSO.',
    author='Leonardo Martins',
    author_email='barretoleonardo111@gmail.com',
    url='https://github.com/yunkzinn/ncs-simplifier', 
    packages=find_packages(),
    install_requires=[
        'ncs', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
