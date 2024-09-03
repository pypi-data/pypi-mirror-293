from setuptools import setup, find_packages

setup(
    name='pojang_resorter',
    version='2.32.3',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pojang-resorter=pojang_resorter.main:main',  # Adjust this based on your main function
        ],
    },
    install_requires=[
        'pillow',
        'pyautogui',
        'requests',
        'discord.py',
        'opencv-python',
        'pycurl',
    ],
)
