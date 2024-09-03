from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='5.5',  # Updated version
    packages=find_packages(),
    install_requires=[
        'pillow',
        'pyautogui',        
        'requests',
        'discord.py',
        'gitpython',
        'opencv-python',
        'pycurl',
        'pywin32',
        'aiohttp',
        'numpy',
        'pygetwindow',
        'pyscreenshot',
        'scipy',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'pojang-resorter = pojang_resorter.main:main',
        ],
    },
    python_requires='>=3.10,<3.13',
    include_package_data=True,
    package_data={
        'pojang_resorter': ['libs/windows.exe'],
    },
)
