__author__ = 'Tim Martin'
from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'tickets', 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='martin-tickets',
    version=version,
    include_package_data=True,
    packages=['tickets', 'ticketsapp'],
    license='Private',
    author='Tim Martin',
    author_email='tim.martin@vertical-knowledge.com',
    description='A web app for managing tickets submitted and completed',
    install_requires=['django', 'djangorestframework', 'django-filter']
)
