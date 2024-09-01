from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="tamil_sentence_extractor", 
    version="0.2",  
    packages=find_packages(),    
    author="Sathishkumar K", 
    author_email="sathish30062002@gmail.com",  
    description="A simple Python module for extracting Tamil sentences from text.",
    long_description=long_description,  
    long_description_content_type="text/markdown", 
    python_requires='>=3.6',  
)