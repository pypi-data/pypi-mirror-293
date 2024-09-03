from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='WSIPeruDB',
    version='0.2.0',
    packages=find_packages(where='.'),
    install_requires=[
       'numpy==1.26.4',
       'pandas==2.2.2',
       'matplotlib==3.9.2',
       'folium==0.14.0',
       'scikit-learn==1.5.1',
       'plotly_express==5.22.0',
       'ipywidgets==8.1.2',
       'geopandas==1.0.1',
       'openpyxl==3.1.5',
       'requests==2.32.3',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    author='Carol Romero',
    author_email='romeroroldancarol@gmail.com',
    description='Water Stable Isotope Database in Peru',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/karoru23/WSI-PeruDB',
)
