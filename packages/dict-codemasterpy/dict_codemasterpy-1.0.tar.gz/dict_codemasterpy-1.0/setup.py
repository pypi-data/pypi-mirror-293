from setuptools import setup, find_packages

setup(
    name='dict_codemasterpy',
    version='1.0',
    packages=find_packages(),  # Позиционный аргумент
    install_requires=['colorama>=0.4.6'],  # Ключевой аргумент
    entry_point ={
      "console_scripts": [
        "dict-codemasterpy = dict_codemasterpy:main",

        ],
    },
)
