from setuptools import setup, find_packages

setup(
    name='polyseq',
    version='1.0',
    description='A package for working with polygons that provides tools for '
                'generating, transforming, filtering, visualizing and aggregating '
                'both finite and infinite sequences of polygons',
    author='Липатников Никита',
    email='lipatnikov.contact@gmail.com',
    packages=find_packages(),
    install_requires=['matplotlib'],
)