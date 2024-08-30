from setuptools import setup, find_packages

setup(
    name='udility',
    version='1.8',
    packages=find_packages(),
    install_requires=[
        'openai',
        'svgwrite',
        'cairosvg',
        'pillow',
        'matplotlib',
    ],
    author='Udit Akhouri',
    author_email='researchudit@gmail.com',
    description='A utility library for generating SVG images from text descriptions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/udility',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)