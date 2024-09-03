from setuptools import setup, find_packages

def main():
    print("Running pojang-resorter...")

setup(
    name='pojang_resorter',
    version='2.31',
    packages=find_packages(),
    include_package_data=True,
    description='A package with a command-line tool',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pojang_resorter',
    entry_points={
        'console_scripts': [
            'pojang-resorter=pojang_resorter.automation:main',
        ],
    },
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
