try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Framework :: Django',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    name='django-pyodbc-lbsm',
    version='1.9.9.1',
    description='Django backend for Microsoft SQL Server with LBSM support',
    long_description=open('README.rst').read(),
    author='Petr Demin',
    author_email='deminp@ncbi.nlm.nih.gov',
    url='https://github.com/michiya/django-pyodbc-azure',
    license='BSD',
    packages=['sql_server_lbsm'],
    install_requires=[
        'Django>=1.9.9,<1.10',
        'sql_server.pyodbc>=1.9.9,<1.10',
    ],
    setup_requires=['wheel'],
    classifiers=CLASSIFIERS,
    keywords='mssql django',
)
