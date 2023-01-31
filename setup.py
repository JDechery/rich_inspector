from setuptools import setup, find_packages

setup(
    name='rich_inspector',
    version='0.1.0',
    url='https://github.com/JDechery/rich_inspector.git',
    author='Joseph Dechery',
    author_email='jdechery@gmail.com',
    description='IPython variable inspector with rich text',
    packages=find_packages(),    
    install_requires=[
        'Pympler>=1.0.1', 
        'ipython~=8.8',
        'rich>=13.0'
    ],
)