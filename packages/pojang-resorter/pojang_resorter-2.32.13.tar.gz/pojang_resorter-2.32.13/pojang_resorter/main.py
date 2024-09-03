import argparse
import subprocess
import logging
from pathlib import Path

# Set up logging
project_dir = Path(__file__).resolve().parent
log_path = project_dir / 'logs' / 'application.log'
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=log_path, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def execute_command_script(command):
    """Execute a command script located in logs/pojang-data."""
    script_path = project_dir / 'logs' / 'pojang-data' / f'{command}.py'
    if script_path.exists():
        try:
            subprocess.run(['python', str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command '{command}': {e}")
            print(f"Failed to execute command '{command}'. Check logs for details.")
    else:
        logging.error(f"Command script '{command}.py' not found.")
        print(f"Command '{command}' not found. Check logs for details.")

def main():
    """Main function to handle command-line arguments and actions."""
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")

    parser.add_argument(
        'command', 
        choices=['screenshot', 'botserver', 'do-snapshot', 'help'],
        help='The command to execute'
    )

    args = parser.parse_args()

    if args.command == 'screenshot':
        execute_command_script('do_snapshot')
    elif args.command == 'botserver':
        execute_command_script('init_bot')
    elif args.command == 'do-snapshot':
        execute_command_script('do_snapshot')
    elif args.command == 'help':
        execute_command_script('show_help')

if __name__ == '__main__':
    main()
