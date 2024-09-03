import argparse
from colorama import init, Fore, Style

# Initialize colorama
init()

def show_help():
    """Show the help information with ASCII art and colors."""
    ascii_art = """
  _____   ____       _         _   _  _____        _____  ______  _____  ____  _____ _______ ______ _____  
 |  __ \ / __ \     | |  /\   | \ | |/ ____|      |  __ \|  ____|/ ____|/ __ \|  __ \__   __|  ____|  __ \ 
 | |__) | |  | |    | | /  \  |  \| | |  __ ______| |__) | |__  | (___ | |  | | |__) | | |  | |__  | |__) |
 |  ___/| |  | |_   | |/ /\ \ | . ` | | |_ |______|  _  /|  __|  \___ \| |  | |  _  /  | |  |  __| |  _  / 
 | |    | |__| | |__| / ____ \| |\  | |__| |      | | \ \| |____ ____) | |__| | | \ \  | |  | |____| | \ \ 
 |_|     \____/ \____/_/    \_\_| \_|\_____|      |_|  \_\______|_____/ \____/|_|  \_\ |_|  |______|_|  \_\
                                                                                                           
    """

    # Define colors
    colors = {
        'header': Fore.MAGENTA,
        'blue': Fore.BLUE,
        'reset': Style.RESET_ALL
    }

    parser = argparse.ArgumentParser(
        description="Python-Mojang Interaction CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command')

    # Define subcommands
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
