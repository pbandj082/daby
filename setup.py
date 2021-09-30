from setuptools import setup

def _get_requires():
    with open('requirements.txt') as f:
        return [p.rstrip() for p in f.readlines()]


setup(
    name='daby',
    version='0.0.3',
    url='https://github.com/pbandj082/daby',
    packages=['daby', 'daby.adapters', 'daby.adapters.asyncpg'],
    requires=_get_requires(),
    extras_requires={
        'dev': ['pytest', 'pytest-asyncio', 'python-dotenv']
    },
)
