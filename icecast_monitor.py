import time
import requests
from bs4 import BeautifulSoup
from plyer import notification

def get_icecast_status(host, port, endpoint, interval_minutes, low_ratio, high_ratio):
    url = f"http://{host}:{port}{endpoint}/status.xsl"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        current_listeners = int(soup.find('listeners').text)
        max_listeners = int(soup.find('listener_peak').text)
        listener_ratio = current_listeners / max_listeners if max_listeners > 0 else 0
        
        if listener_ratio < low_ratio:
            message = f"Low listener ratio detected: {listener_ratio:.2%}"
            send_notification("Icecast Notification", message)
        elif listener_ratio > high_ratio:
            message = f"High listener ratio detected: {listener_ratio:.2%}"
            send_notification("Icecast Notification", message)
    except Exception as e:
        print(f"Failed to connect to Icecast server: {e}")

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10  # Notification timeout in seconds
    )

def main():
    host = input("Enter the Icecast server host (e.g., us2.ishout.net): ")
    port = input("Enter the Icecast server port (default is 8000): ")
    endpoint = input("Enter the endpoint for status information (e.g., 'live' or 'listen'): ")
    low_ratio = float(input("Enter the low listener ratio threshold (e.g., 0.1 for 10%): "))
    high_ratio = float(input("Enter the high listener ratio threshold (e.g., 0.9 for 90%): "))
    interval_minutes = int(input("Enter the monitoring interval in minutes: "))
    
    while True:
        get_icecast_status(host, port, endpoint, interval_minutes, low_ratio, high_ratio)
        time.sleep(interval_minutes * 60)  # Sleep for the specified interval

if __name__ == "__main__":
    main()
