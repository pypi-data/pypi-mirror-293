import argparse
import subprocess
import logging
from pathlib import Path

# Set up logging
log_path = Path(__file__).resolve().parent / 'logs' / 'application.log'
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=log_path, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def execute_command_script(command):
    """Execute a command script located in the same directory as main.py."""
    command_map = {
        'screenshot': 'do_snapshot',
        'botserver': 'init_bot',
        'do-snapshot': 'do_snapshot',
        'help': 'show_help'
    }
    script_name = command_map.get(command)
    if script_name:
        script_path = Path(__file__).resolve().parent / f'{script_name}.py'
        if script_path.exists():
            try:
                subprocess.run(['python', str(script_path)], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error executing command '{command}': {e}")
                print(f"Failed to execute command '{command}'. Check logs for details.")
        else:
            logging.error(f"Command script '{script_name}.py' not found.")
            print(f"Command '{command}' not found. Check logs for details.")
    else:
        logging.error(f"Unknown command '{command}'.")
        print(f"Unknown command '{command}'. Check logs for details.")

def main():
    """Main function to handle command-line arguments and actions."""
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")
    parser.add_argument(
        'command', 
        choices=['screenshot', 'botserver', 'do-snapshot', 'help'],
        help='The command to execute'
    )

    args = parser.parse_args()
    execute_command_script(args.command)

if __name__ == '__main__':
    main()
