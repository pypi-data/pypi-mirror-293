import argparse
import subprocess
import logging
from pathlib import Path
import sys  # Import sys to check command-line arguments

# Set up logging
log_path = Path(__file__).resolve().parent / 'logs' / 'application.log'
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=log_path, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def execute_command_script(command):
    """Execute a command script located in the same directory as the main script."""
    command_map = {
        'initialize_server': 'init_bot',
        'preview_server': 'do_snapshot',
        'display_help': 'show_help',
        'assign_operator': 'forceop'
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
    parser = argparse.ArgumentParser(description="Python-Mojang Interaction CLI Tool")
    parser.add_argument(
        'command', 
        nargs='?',  # Allow the command argument to be optional
        choices=['initialize_server', 'preview_server', 'display_help', 'assign_operator'],
        help='The command to execute'
    )

    args = parser.parse_args()
    
    # If no command is provided, default to 'initialize_server'
    if args.command is None:
        args.command = 'initialize_server'
    
    execute_command_script(args.command)

if __name__ == '__main__':
    main()
