from setuptools import setup, find_packages

setup(
    name='Udility',  # Package name
    version='2.0',
    author='Udit Akhouri',
    author_email='researchudit@gmail.com',
    description='A diffuser to generate illustrative images based on Meta Llama 3.5.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/Udility',  # Replace with your GitHub repository URL
    packages=find_packages(),
    install_requires=[
        'openai',
        'cairosvg',
        'Pillow',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
