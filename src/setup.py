from setuptools import setup
setup(
    name = 'notery3',
    version = '0.0.0',
    packages = ['notery3'],
    entry_points = {
        'console_scripts': [
            'notery3 = notery3.__main__:main'
        ]
    })