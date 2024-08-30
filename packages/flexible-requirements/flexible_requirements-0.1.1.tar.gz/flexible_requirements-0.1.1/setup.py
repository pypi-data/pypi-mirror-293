from setuptools import setup, find_packages

setup(
    name='flexible_requirements',
    version='0.1.1',
    author='benny-png',
    author_email='mazikuben2@gmail.com',
    description='A library for generating flexible Python requirements',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/benny-png/Flexible-Requirements-python-LIBRARY',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=open('own_requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
