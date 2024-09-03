from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='2.32.12',
    packages=find_packages(),
    install_requires=[
        'pillow',
        'pyautogui',
        'requests',
        'discord.py',
        'gitpython',  # This should be used instead of 'git' for interacting with Git in Python
        'opencv-python',
        'pycurl',
        'pywin32',  # Required for creating shortcuts on Windows
    ],
    entry_points={
        'console_scripts': [
            'pojang-resorter = pojang_resorter.main:main',
        ],
    },
    python_requires='>=3.12',  # Specify the Python version compatibility
)
