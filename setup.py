from setuptools import setup

setup(
    name='SimpleCapp Calculation Engine',
    url='https://github.com/GustavoRonconi/simplecapp_calculation_engine',
    author='Gustavo A. Ronconi',
    author_email='gustavo.ronconi@simplecapp.com.br',
    packages=['calculation_engine'],
    install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)