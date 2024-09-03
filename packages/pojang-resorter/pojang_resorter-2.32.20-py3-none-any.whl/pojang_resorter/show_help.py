import argparse
import sys

def show_help():
    """Show the help information with ASCII art and colors."""
    ascii_art = """
    _____           _           
   |  __ \\         | |          
   | |__) |___  ___| | ___ _ __ 
   |  _  // _ \\/ __| |/ _ \\ '__|
   | | \\ \\  __/\\__ \\ |  __/ |   
   |_|  \\_\\___||___/_|\\___|_|   
                                 
    """

    colors = {
        'header': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'warning': '\033[93m',
        'fail': '\033[91m',
        'reset': '\033[0m'
    }

    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")
    parser.add_argument(
        'command',
        choices=['initialize_server', 'preview_server', 'display_help', 'assign_operator'],
        help='The command to execute'
    )

    # Print ASCII Art and colored header
    print(colors['header'] + ascii_art + colors['reset'])
    print(colors['blue'] + "Available Commands:" + colors['reset'])
    
    parser.print_help()

if __name__ == "__main__":
    show_help()
