from setuptools import setup, find_packages

setup(
    name='indomaret',  # Nama package di PyPI
    version='1.0.0',  # Versi package kamu
    packages=find_packages(),  # Secara otomatis menemukan semua packages
    entry_points={
        'console_scripts': [
            'ess=tes.ess:main',  # Nama command-line dan fungsi utama
        ],
    },
    install_requires=[
        # Daftar dependensi, jika ada
    ],
    description='hanya sebuah script biasa',
    author='robbi 13',
    author_email='email@example.com',
    url='https://github.com/username/my_project',  # URL repositori atau website
)
