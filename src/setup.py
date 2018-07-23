from setuptools import setup
setup(
    name = 'notery',
    version = '0.0.0',
    packages = ['notery'],
    entry_points = { 'console_scripts': [
        'notery = notery.__main__:main'
    ]},

    author="Henry Blanchette",
    description="An alternative for Latex offering better automation and modularity.",
    url="https://github.com/Riib11/Notery"
)