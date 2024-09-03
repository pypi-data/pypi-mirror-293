import argparse
import subprocess
import logging

def main():
    """Main function to handle command-line arguments and actions."""
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")

    parser.add_argument(
        'command', 
        choices=['do-snapshot', 'init-bot', 'show-help'],
        help='The command to execute'
    )

    args = parser.parse_args()

    try:
        if args.command == 'do-snapshot':
            subprocess.run(["python", "logs/pojang-data/do_snapshot.py"], check=True)
        elif args.command == 'init-bot':
            subprocess.run(["python", "logs/pojang-data/init_bot.py"], check=True)
        elif args.command == 'show-help':
            subprocess.run(["python", "logs/pojang-data/show_help.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command '{args.command}': {e}")

if __name__ == '__main__':
    main()
