# setup.py
from setuptools import setup, find_packages

setup(
    name='kheops',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas==2.0.0',
        'tqdm==4.66.5',
        'langchain-community==0.2.12',
        'langchain==0.2.14',
        
        # List any other dependencies your package requires here
    ],
    entry_points={
        'console_scripts': [
            # 'command-name = your_package_name.module:function'
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for generating responses with an LLM and evaluating them on MMLU.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',  # Replace with your GitHub repository link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',

)
