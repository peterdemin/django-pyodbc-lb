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
    name='django-pyodbc-lb',
    version='1.11.0.0',
    description='Django backend for Microsoft SQL Server with load balancer support',
    long_description=open('README.rst').read(),
    author='Petr Demin',
    author_email='deminp@ncbi.nlm.nih.gov',
    url='https://github.com/peterdemin/django-pyodbc-lb',
    license='BSD',
    packages=['sql_server_lb'],
    install_requires=[
        'Django>=1.11,<1.12',
        'django-pyodbc-azure>=1.11,<1.12',
    ],
    setup_requires=['wheel'],
    classifiers=CLASSIFIERS,
    keywords='mssql django',
)
