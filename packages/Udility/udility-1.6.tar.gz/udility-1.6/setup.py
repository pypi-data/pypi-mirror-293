from setuptools import setup, find_packages

setup(
    name='udility',
    version='1.6',
    packages=find_packages(),
    install_requires=[
        'openai',
        'cairosvg',
        'Pillow',
        'matplotlib'
    ],
    description='A Python library for generating SVG illustrations using AI.',
    author='Udit Akhouri',
    author_email='researchudit@gmail.com',
    url='https://github.com/uditakhourii/udility',  # Replace with your GitHub repo URL
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
