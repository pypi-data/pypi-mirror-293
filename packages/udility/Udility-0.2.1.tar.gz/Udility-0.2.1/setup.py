# setup.py

from setuptools import setup, find_packages

# Read the content of README.md for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Udility',
    version='0.2.1',  # Increment version number
    author='Udit Akhouri',
    author_email='researchudit@gmail.com',
    description='A unified API for generating illustrations and animations using AI and OpenRouter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/udility',  # Replace with your actual URL
    packages=find_packages(),
    install_requires=[
        'openai',
        'cairosvg',  # Python bindings for SVG handling
        'pillow',  # Image processing library
        'matplotlib',  # Library for plotting images
        'selenium',  # Web driver for animations
        'pymongo',  # MongoDB client for Python
        'dnspython',  # DNS toolkit for Python (required by pymongo)
        'werkzeug',  # Security and utilities for Python
        'pycairo',  # Python bindings for cairo graphics library
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
