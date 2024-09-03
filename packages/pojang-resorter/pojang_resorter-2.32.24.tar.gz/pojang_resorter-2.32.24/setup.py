from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='2.32.24',
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
)
