from setuptools import setup, find_packages

setup(
    name='readme_gen',
    version='0.1',
    packages=find_packages(),
    description='A simple package to generate README files for projects automatically.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Indicates the format of long_description
    author='Eshan Iqbal',
    author_email='mireshan321@gmail.com',
    url='https://github.com/Eshaniqbal/Readme_gen-Package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        # List your package dependencies here
    ],
)
