import importlib
import traceback
import time
import subprocess
import requests
from xml.etree import ElementTree as ET
from pynotifier import Notification  # Import 'pynotifier'

def check_and_install_libraries(required_libraries):
    print("Checking for needed libraries, please wait...")
    missing_libraries = [lib for lib in required_libraries if importlib.util.find_spec(lib) is None]

    if missing_libraries:
        print("The following required libraries are missing:")
        for lib in missing_libraries:
            print(lib)

        install_libraries = input("Do you want to install these libraries now, including pynotifier? (y/n): ").lower()

        if install_libraries == 'y':
            try:
                for lib in missing_libraries:
                    try:
                        subprocess.check_call(['pip', 'install', lib])
                        print(f"{lib} installed successfully.")
                    except subprocess.CalledProcessError as e:
                        print(f"Error installing {lib}: {e}")

                # Install pynotifier
                try:
                    subprocess.check_call(['pip', 'install', 'py-notifier'])
                    print("py-notifier installed. You can receive desktop notifications.")
                except subprocess.CalledProcessError as e:
                    print(f"Error installing py-notifier: {e}")

                if not missing_libraries:
                    print("All required libraries are now installed.")

            except Exception as e:
                print(f"Error during installation: {e}")
                traceback.print_exc()  # Print the traceback
                return False
        else:
            print("Please install the required libraries manually and then run the script again.")
            return False

    return True

def send_notification(title, message):
    Notification(title, message).send()

required_libraries = ['requests', 'xml.etree.ElementTree']

def get_icecast_status(host, port, interval_minutes):
    url = f"http://{host}:{port}/status.xsl"

    while True:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Parse the XML response
                root = ET.fromstring(response.text)

                # Extract relevant information
                current_listeners = int(root.find("listeners").text)
                peak_listeners = int(root.find("listener_peak").text)

                print("Icecast Server Status:")
                print(f"Current Listeners: {current_listeners}")
                print(f"Peak Listeners: {peak_listeners}")

                if current_listeners < 10:
                    send_notification("Low Listener Count", f"Current Listener Count: {current_listeners}")
                elif current_listeners > 100:
                    send_notification("High Listener Count", f"Current Listener Count: {current_listeners}")

                # You can extract and print more information if needed

            else:
                print(f"Failed to retrieve Icecast status. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to Icecast server: {e}")

        time.sleep(interval_minutes * 60)  # Sleep for the specified interval

def main():
    if check_and_install_libraries(required_libraries):
        print("Welcome to the Icecast Server Status Monitor.")
        host = input("Enter the Icecast server host (e.g., us2.ishout.net): ")
        port = input("Enter the Icecast server port (default is 8000): ")

        if not port:
            port = "8000"

        print("\n**IMPORTANT: Monitoring the Icecast server allows you to track its status and usage over time. However, please be aware of the following considerations:**")
        print("1. Frequent monitoring may lead to rate limiting or banning from the server.")
        print("2. Excessive monitoring can place additional load on the server and affect its performance.")
        print("3. Consider your monitoring interval carefully to balance your need for real-time data with the server's capacity.")
        print("4. If you are not the server administrator, ensure that your monitoring is in compliance with the server's policies and guidelines.")
        
        interval_minutes = int(input("Enter the monitoring interval in minutes: ")

        get_icecast_status(host, port, interval_minutes)

if __name__ == "__main__":
    main()
