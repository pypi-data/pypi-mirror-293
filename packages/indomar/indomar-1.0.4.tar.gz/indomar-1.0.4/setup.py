from setuptools import setup, find_packages

setup(
    name='indomar',  # Nama package di PyPI
    version='1.0.4',  # Versi package kamu
    packages=find_packages(),  # Secara otomatis menemukan semua packages
    entry_points={
        'console_scripts': [
            'idm=idm.idm:main',  # Nama command-line dan fungsi utama
        ],
    },
    install_requires=[
        'aiohttp',
        'requests',
    ],
    description='hanya sebuah script biasa',
    author='robbi 13',
    author_email='email@example.com',
    url='https://github.com/username/my_project',  # URL repositori atau website
)
