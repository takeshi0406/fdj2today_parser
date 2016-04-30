from setuptools import setup, find_packages

setup(
    name='fdj2today_parser',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'feedparser'
    ]
)
