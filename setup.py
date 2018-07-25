from setuptools import setup, find_packages

setup(name='copyright-updater',
    version=0.1,
    description='Simple tool to update the copyright in C and Python files',
    url='https://github.com/swasun/copyright-updater',
    author='Charly Lamothe',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [ 'copyright-updater=copyright_updater.__main__:main']
    }
)