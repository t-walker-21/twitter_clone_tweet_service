from setuptools import setup, find_packages
  
setup( 
    name='tweet_crud', 
    version='1.0', 
    description='A simple crud app replicating a simplistic tweet service', 
    author='Tevon Walker',  
    packages= find_packages(where='src'),
) 
