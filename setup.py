from setuptools import setup, find_packages

setup(
    name='polyseq',
    version='1.0',
    description='A package for working with polygons that provides tools for '
                'generating, transforming, filtering, visualizing and aggregating '
                'both finite and infinite sequences of polygons',
    #long_description=open('').read(),
    #long_description_content_type=
    author='Липатников Никита',
    packages=find_packages(),
    install_requires=['matplotlib'],
)