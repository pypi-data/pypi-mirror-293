import argparse
import sys

def show_help():
    """Show the help information with modern ASCII art and colors."""
    ascii_art = """
  ____        _               ____                 
 |  _ \\  __ _| |_   ___  __  |  _ \\  ___  _ __ ___ 
 | |_) |/ _` | \\ \\ / / |/ /  | |_) |/ _ \\| '__/ _ \\
 |  _ <| (_| | |\\ V /|   <   |  __/|  __/| | |  __/
 |_| \\_\\__,_|_| \\_/ |_|\\_\\  |_|    \\___||_|  \\___|
                                                 
    """

    colors = {
        'header': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'reset': '\033[0m'
    }

    parser = argparse.ArgumentParser(description="Python-Mojang Interaction CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    # Subcommands with descriptions
    subparsers.add_parser('initialize_server', help='Initialize the server and start the bot.')
    subparsers.add_parser('preview_server', help='Preview the current server status or snapshot.')
    subparsers.add_parser('display_help', help='Display this help message with command details.')
    subparsers.add_parser('assign_operator', help='Assign operator privileges to a user.')

    # Print ASCII Art and colored header
    print(colors['header'] + ascii_art + colors['reset'])
    print(colors['blue'] + "Available Commands:" + colors['reset'])
    
    parser.print_help()

if __name__ == "__main__":
    show_help()
