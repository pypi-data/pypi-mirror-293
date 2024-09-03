from setuptools import setup, find_packages

setup(
    name='document_reader',  # Nom de votre package
    version='0.1.0',  # Version de votre package
    author='Joris PHILIPPOTEAUX',
    author_email='joris.philippoteaux@bearingpoint.com',
    description='Read several document format to output a markdown like python string',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Format du fichier README
    url='https://github.com/joris-philippoteaux-BE/document_reader.git',  # URL de votre projet
    packages=find_packages(),  # Trouver et inclure tous les packages Python
    classifiers=[  # Informations supplémentaires sur votre package
        'Programming Language :: Python :: 3.11'
        
    ]
    
)