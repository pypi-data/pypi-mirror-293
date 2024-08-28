# setup.py

from setuptools import setup, find_packages

setup(
    name='X_Scraper', 
    version='0.1.0',  
    author='Saikat Singha',
    author_email='saikatsingha00q@gmail.com',
    description='A Python module to scrape Twitter posts and images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Saikat-too/Scraper', 
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',  
        'beautifulsoup4',
        'selenium',
        'time ',
        'tqdm',
        're',
        'urllib.request',
        
    ],
)
