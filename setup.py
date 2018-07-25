from setuptools import setup

setup(name='copyright-updater',
    version=0.1,
    description='Simple tool to update the copyright in C and Python files',
    url='https://github.com/swasun/copyright-updater',
    author='Charly Lamothe',
    license='MIT',
    packages=['copyright_updater'],
    package_data={'copyright_updater': ['templates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [ 'copyright-updater=copyright_updater.__main__:main']
    }
)