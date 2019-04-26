from setuptools import setup, find_packages

setup(
    name='expressionable-cli',
    url='https://github.com/srp33/ExpressionAble-CLI',
    author='Piccolo Lab',
    author_email='stephen_piccolo@byu.edu',
    packages=find_packages(),
    entry_points = {
        "console_scripts": ['expressionable = expressionablecli.expressionablecli:main',
                            'ea = expressionablecli.expressionablecli:main',
                            'eable = expressionablecli.expressionablecli:main',
                            'expressionablemerge = mergecli.mergecli:main',
                            'merge = mergecli.mergecli:main',
                            'eamerge = mergecli.mergecli:main']
        },
    install_requires=['expressionable>=1.2','pandas'],
    version=open('VERSION').read().strip(),
    license='MIT',
    description='A command-line tool for transforming large data sets',
    long_description=open('README.md').read(),
)
