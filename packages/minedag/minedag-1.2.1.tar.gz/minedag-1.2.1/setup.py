import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='minedag',
    version='1.2.1',
    author='Komissarov Andrey',
    author_email='Komissar.off.andrey@gmail.com',
    description='Mine realisation of DAG',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moff4/minedag',
    install_requires=[
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
)
