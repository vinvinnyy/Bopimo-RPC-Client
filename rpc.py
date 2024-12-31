import pypresence
import time
import pygetwindow as gw
import psutil

client_id = "XXXXXXXXXXXXXXXX"  # Replace with your actual client ID

pcsv2 = "Bopimo!"  # Substring to look for in window title

# Function to find windows by title
def find_windows_by_name(substring):
    matching_windows = []
    
    # Iterate through all windows
    for window in gw.getAllWindows():
        if substring.lower() in window.title.lower():  # Check if the substring matches the title
            matching_windows.append(window)
    
    return matching_windows

# Function to get the PID from the window title using psutil
def get_pid_from_window(window):
    # Search for the process by window title
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if window.title.lower() in proc.info['name'].lower():
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

# Initialize the pypresence client
try:
    client = pypresence.Presence(client_id)  # Initialize the client with your client_id
    client.connect()  # Connect to Discord

    large_image = "https://i.ibb.co/8s7pP3t/favicons.png"  # (Yes you can replace this as anything)
    # While loop to keep checking every 0.5 seconds and update presence based on window
    while True:
        windows = find_windows_by_name(pcsv2)
        if windows:
            print(f"Found {len(windows)} window(s) matching '{pcsv2}':")
            for window in windows:  # This is actually gets your browser window because it finds all windows containing "Bopimo!"
                # Optionally, get the process ID (PID) if needed
                pid = get_pid_from_window(window)
                print(f"- {window.title} (PID: {pid})" if pid else f"- {window.title} (PID not found)")
            
            # Update Discord presence if the game window is found
            client.update(
                state="In Bopimo!",
                details="Playing/Viewing Bopimo!", # Viewing Bopimo! means your seeing the website aswell
                large_image=large_image,  # Set the large image
                large_text="Bopimo!",  # Tooltip for large image
            )
        else:
            print(f"No windows found matching '{pcsv2}' (This might find browser tab aswell.)")
            client.update()

        # Wait for 0.5 seconds before checking again
        time.sleep(0.1)

except Exception as e:
    print(f"Error initializing pypresence: {e}")
