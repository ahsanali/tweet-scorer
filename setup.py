# -*- coding: utf-8 -*-

from setuptools import setup

project = "slow twitter client"

setup(
    name='slow twitter client',
    version='0.1',
    url='',
    description='',
    author='Ahsan Ali',
    author_email='sn.ahsanali@gmail.com',
    packages=["app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==0.9',
        'flask-login',
        'flask-openid',
        'flask-mail==0.7.6',
        'sqlalchemy==0.7.9',
        'flask-sqlalchemy==0.16',
        'sqlalchemy-migrate==0.7.2',
        'flask-whooshalchemy==0.54a',
        'flask-wtf==0.8.4',
        'pytz==2013b',
        'flask-babel==0.8',
        'flup',
        'Flask-OAuthlib',
        'Flask-Script'

    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Slow Twitter Client Developers and Stake Holders',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)

