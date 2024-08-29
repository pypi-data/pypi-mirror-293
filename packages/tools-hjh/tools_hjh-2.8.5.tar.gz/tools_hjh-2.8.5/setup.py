from setuptools import setup

setup (
    name='tools_hjh',
    version='2.8.5',
    author='HuaJunhao',
    author_email='huajunhao6@yeah.net',
    install_requires=[
          'dbutils'
        # , 'pillow'
        , 'pymysql'
        , 'psycopg2'
        , 'cx_Oracle'
        , 'paramiko'
        , 'pandas'
        # , 'crypto'
        , 'requests'
        # , 'selenium'
        , 'eventlet'
    ],
    packages=['tools_hjh', 'other']
)
