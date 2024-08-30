# setup.py

from setuptools import setup, find_packages

setup(
    name='Udility',
    version='0.2.5',  # Increment the version number
    author='Udit Akhouri',
    author_email='researchudit@gmail.com',
    description='A unified API for generating illustrations and animations using AI and OpenRouter.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/udility',  # Replace with your actual URL
    packages=find_packages(),
    install_requires=[
        'openai',
        'cairosvg',
        'pillow',
        'matplotlib',
        'pymongo',
        'dnspython',
        'werkzeug'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
