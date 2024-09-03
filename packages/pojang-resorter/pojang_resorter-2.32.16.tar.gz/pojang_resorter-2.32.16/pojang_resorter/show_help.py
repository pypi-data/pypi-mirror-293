import argparse

def show_help():
    """Show the help information."""
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI Tool")
    parser.add_argument(
        'command',
        choices=['screenshot', 'botserver', 'do-snapshot', 'help'],
        help='The command to execute'
    )
    parser.print_help()

if __name__ == "__main__":
    show_help()
