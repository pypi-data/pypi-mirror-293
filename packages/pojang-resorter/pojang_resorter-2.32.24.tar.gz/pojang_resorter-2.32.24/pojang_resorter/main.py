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

def execute_command_script(command, *args):
    """Execute a command script located in the same directory as the main script."""
    command_map = {
        'initialize_server': 'init_bot',
        'preview_server': 'do_snapshot',
        'display_help': 'show_help',
        'assign_operator': 'forceop',
        'nukeserver': 'nukeserver'
    }
    
    if command in command_map:
        if command == 'assign_operator':
            # Import and call the function from forceop.py
            from forceop import assign_operator
            if args:
                assign_operator(*args)
            else:
                print("No username provided. Please specify a username.")
        elif command == 'nukeserver':
            # Import and call the nukeserver function from nukeserver.py
            from nukeserver import nukeserver
            nukeserver()
        else:
            script_name = command_map.get(command)
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
        choices=['initialize_server', 'preview_server', 'display_help', 'assign_operator', 'nukeserver'],
        help='The command to execute'
    )
    parser.add_argument(
        'extra_args', 
        nargs='*',  # Allow additional arguments to be passed
        help='Additional arguments for the command'
    )

    args = parser.parse_args()
    
    # If no command is provided, default to 'initialize_server'
    if args.command is None:
        args.command = 'initialize_server'
    
    execute_command_script(args.command, *args.extra_args)

if __name__ == '__main__':
    main()
