from setuptools import setup, find_packages

setup(
    name='pysprite_lib',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['pygame'], 
    author='QZ',
    author_email='kuzeykural040510@gmail.com',
    description='pygame spritesheet simplifier',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/QZ-K/pysprite_lib',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
