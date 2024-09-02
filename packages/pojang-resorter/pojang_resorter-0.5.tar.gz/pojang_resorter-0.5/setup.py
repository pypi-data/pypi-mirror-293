from setuptools import setup, find_packages
from custom_install import CustomInstall

setup(
    name='pojang_resorter',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'requests'
    ],
    cmdclass={
        'install': CustomInstall,
    },
)
