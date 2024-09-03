import argparse
import logging
from mcrcon import MCRcon

# Configure logging
logging.basicConfig(filename='assign_operator.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def assign_operator(username, server_ip, rcon_port, rcon_password):
    """Assign operator privileges to a user on the Minecraft server."""
    if not username:
        print("No username provided. Please specify a username.")
        return
    
    try:
        logging.info(f"Connecting to Minecraft server at {server_ip}:{rcon_port}")
        with MCRcon(server_ip, rcon_password, port=rcon_port) as mcr:
            response = mcr.command(f"op {username}")
            if "error" in response.lower():
                logging.error(f"Failed to assign operator privileges to {username}. Response: {response}")
                print(f"Failed to assign operator privileges to {username}.")
            else:
                logging.info(f"Successfully assigned operator privileges to {username}.")
                print(f"Assigned operator privileges to {username}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assign operator privileges to a user on a Minecraft server")
    parser.add_argument('username', help='The username to assign operator privileges to')
    parser.add_argument('server_ip', help='The IP address of the Minecraft server')
    parser.add_argument('rcon_port', type=int, help='The RCON port of the Minecraft server')
    parser.add_argument('rcon_password', help='The RCON password of the Minecraft server')
    args = parser.parse_args()
    assign_operator(args.username, args.server_ip, args.rcon_port, args.rcon_password)
