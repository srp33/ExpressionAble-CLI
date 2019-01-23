from setuptools import setup, find_packages

setup(
    name='shapeshifter-cli',
    url='https://github.com/srp33/ShapeShifter-CLI',
    author='Piccolo Lab',
    author_email='stephen_piccolo@byu.edu',
    packages=find_packages(),
    entry_points = {
        "console_scripts": ['shapeshift = shapeshiftercli.shapeshiftercli:main',
                            'ss = shapeshiftercli.shapeshiftercli:main',
                            'shapeshiftmerge = shapeshiftercli.mergecli:main',
                            'ssm = shapeshiftercli.mergecli:main'] #add one for merge?
        },
    install_requires=['shapeshifter','pandas'],
    version=open('VERSION').read().strip(),
    license='MIT',
    description='A command-line tool for transforming large data sets',
    long_description=open('README.md').read(),
)
