import requests

def check_server_status(server_type, host, port, mount):
    """
    Function to check server status.
    Args:
        server_type (str): Server type (Icecast/Shoutcast).
        host (str): Host (IPv4 address or domain name).
        port (int): Port number.
        mount (str): Mount point.

    Returns:
        tuple: A tuple containing success flag (bool) and listeners count (int).
    """
    success = False
    listeners = 0
    try:
        # Check if host input is provided
        if not host:
            raise ValueError("Host is required.")
        
        # Make HTTP GET request to server API or status checking endpoint
        if server_type == "Icecast":
            url = f"http://{host}:{port}/status-json.xsl"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                json_response = response.json()
                for source in json_response['icestats']['source']:
                    if source['mount'] == f'/{mount}':
                        success = True
                        listeners = int(source['listeners'])
                        break
            else:
                success = False
        elif server_type == "Shoutcast":
            url = f"http://{host}:{port}/admin.cgi?json=1&mode=viewxml&pass={mount}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                json_response = response.json()
                if 'currentlisteners' in json_response:
                    success = True
                    listeners = int(json_response['currentlisteners'])
            else:
                success = False
        else:
            raise ValueError("Invalid server type. Must be 'Icecast' or 'Shoutcast'")
    except Exception as e:
        success = False

    return success, listeners
