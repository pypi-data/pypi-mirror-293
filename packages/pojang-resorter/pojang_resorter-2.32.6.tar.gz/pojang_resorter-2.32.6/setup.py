from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='2.32.6',
    packages=find_packages(),
    install_requires=[
        'pillow',
        'pyautogui',
        'requests',
        'discord.py',
        'opencv-python',
        'pycurl'
    ],
    entry_points={
        'console_scripts': [
            'pojang-resorter=pojang_resorter.main:main',
        ],
    },
    python_requires='>=3.6',  # Specify the Python version compatibility
)
