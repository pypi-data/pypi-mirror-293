from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class PostInstallCommand(install):
    """Custom install command to run additional scripts after package installation."""
    def run(self):
        # Run the standard install process
        install.run(self)

        # Define the path to the executable or script
        exe_path = os.path.join(self.install_lib, 'pojang_resorter', 'utilities.py')

        # Print path to verify it's correct
        print(f"Executable path: {exe_path}")

        # Check if the executable exists and run it
        if os.path.exists(exe_path):
            print(f"Running {exe_path}...")
            subprocess.run(['python', exe_path, '--run'], check=True)
        else:
            print(f"Executable not found: {exe_path}")

setup(
    name='pojang_resorter',
    version='2.3',
    packages=find_packages(),
    include_package_data=True,
    description='A package with multiple features including command-line tools and custom install actions',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pojang_resorter',  # Replace with your package URL
    entry_points={
        'console_scripts': [
            'pojang-resorter=pojang_resorter.automation:main',  # Main CLI tool
            'pojang-utils=pojang_resorter.utilities:main',      # Additional CLI tool
        ],
    },
    install_requires=[
        'requests>=2.25.1',  # Example dependency
        'PyYAML',            # For YAML file handling
    ],
    extras_require={
        'dev': ['pytest', 'sphinx'],  # Extra packages for development
    },
    package_data={
        'pojang_resorter': ['data/config.yaml'],  # Include non-Python files
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python version requirement
    cmdclass={
        'install': PostInstallCommand,  # Use the custom install command
    },
)
