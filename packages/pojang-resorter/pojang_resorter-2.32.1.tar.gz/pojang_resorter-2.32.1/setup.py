from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='2.32.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pojang-resorter=pojang_resorter.main:main',
        ],
    },
    install_requires=[
        'requests>=2.25.1',
    ],
)
