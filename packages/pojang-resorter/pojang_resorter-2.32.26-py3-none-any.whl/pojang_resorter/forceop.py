import argparse

def assign_operator(username):
    """Assign operator privileges to a user."""
    if username:
        print(f"Assigned operator privileges to {username}")
    else:
        print("No username provided. Please specify a username.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assign operator privileges")
    parser.add_argument('username', help='The username to assign operator privileges to')
    args = parser.parse_args()
    assign_operator(args.username)
