import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Pojang Resorter CLI")
    parser.add_argument('action', help="Action to perform")
    args = parser.parse_args()

    if args.action == 'do_something':
        print("Doing something...")
    else:
        print("Unknown action")

if __name__ == '__main__':
    main()
