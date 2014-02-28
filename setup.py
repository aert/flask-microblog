from setuptools import setup, find_packages


setup(
    name='microblog',
    version='0.4',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/aert/flask-microblog',
    license='MIT',
    author='aert',
    author_email='dev.aert@gmail.com',
    description='Learning Flask.'
)
