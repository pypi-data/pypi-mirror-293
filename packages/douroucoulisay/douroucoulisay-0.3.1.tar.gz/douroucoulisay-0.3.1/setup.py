from setuptools import setup, find_packages

setup(
    name='douroucoulisay',
    version='0.3.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'douroucoulisay=douroucoulisay.douroucoulisay:douroucoulisay',  # Replace `your_module` with the actual module name
        ],
    },
    install_requires=[],  # List dependencies here if needed
    include_package_data=True,
    package_data={
        '': ['assets/*.txt'],
    },
    author='Aotus Parisinus',
    author_email='douroucoulis-fr@gmail.com',
    description='A package to print messages with douroucoulis ASCII art.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/douroucoulis-fr/douroucoulisay',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
