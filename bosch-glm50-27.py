from bluepy import btle
import struct
import pyperclip
import os
import time
import sys
import pyautogui

# Global variables
debug_mode = False  # Set debug mode to False by default
verbose = False  # Default verbose mode
separator = "comma"  # Default separator

class LaserDelegate(btle.DefaultDelegate):
    def __init__(self, insert_type):
        super().__init__()
        self.insert_type = insert_type

    def handleNotification(self, cHandle, data):
        hex_values = data.hex()  # Convert the received data to hex format
        if verbose:  # Only print if verbose mode is enabled
            print("Indication received:", hex_values)
        measurement_value = print_response(hex_values, self.insert_type)  # Pass insert_type to the response processing
        if measurement_value is not None:
            # Format the measurement value based on the separator
            if separator == "point":
                formatted_value = str(measurement_value).replace(',', '.')
            else:
                formatted_value = str(measurement_value)

            if verbose: 
                print(f"Formatted measurement value: {formatted_value}")  # Example output

def connect_to_laser(mac_address):
    print(f"Connecting to laser with MAC address {mac_address}...")
    device = btle.Peripheral(mac_address)  # Create a Bluetooth peripheral object
    print("Connection successful.")
    return device

def write_characteristic(device, handle, value):
    device.writeCharacteristic(handle, bytes.fromhex(value))  # Write value to the specified characteristic

def hex_to_float(hex_value):
    unsigned_int = int(hex_value, 16)  # Convert hex to unsigned integer
    packed = struct.pack('I', unsigned_int)  # Pack the integer into bytes
    float_converted = struct.unpack('f', packed)[0]  # Unpack bytes as a float
    return float_converted

def print_response(hex_values, insert_type):
    global debug_mode
    if debug_mode: 
        print("hex_values", hex_values)  # Print hex values if in debug mode
    formatted_hex = [hex_values[i:i+2] for i in range(0, len(hex_values), 2)]  # Format hex values into pairs
    if debug_mode: 
        print("formatted_hex:", formatted_hex)

    # Check if the response is valid
    if formatted_hex[0] == "c0" and formatted_hex[1] == "55" and formatted_hex[2] == "10" and formatted_hex[3] == "06":
        measurement_hex = formatted_hex[7:11]  # Extract the measurement part of the response
        measurement_hex.reverse()  # Reverse the order of the hex values
        measurement_hex_value = ''.join(measurement_hex)  # Join hex values into a single string
        measurement_value = hex_to_float(measurement_hex_value)  # Convert hex to float
        measurement_value_cm = measurement_value * 100  # Convert to centimeters
        measurement_value_cm_rounded = round(measurement_value_cm, 1)  # Round to one decimal place
        
        # Format the measurement value based on the separator
        if separator == "comma":
            measurement_value_cm_rounded_str = str(measurement_value_cm_rounded).replace('.', ',')
        else:
            measurement_value_cm_rounded_str = str(measurement_value_cm_rounded)

        pyperclip.copy(measurement_value_cm_rounded_str)  # Copy the measurement to the clipboard
        if verbose: 
            print(f"Measured length: {measurement_value_cm_rounded_str} (copied to clipboard)")

        # Insert the value at the current cursor position
        time.sleep(0.2)  # Wait to ensure the clipboard is ready
        pyautogui.hotkey('ctrl', 'v')  # Simulate Ctrl+V to paste
        time.sleep(0.2)  # Wait to ensure the clipboard is ready
        
        # Insert the desired text based on the specified insertion type
        if insert_type == "Enter":
            pyautogui.press('enter')
        elif insert_type == "Tab":
            pyautogui.press('tab')
        elif insert_type == "Comma":
            pyautogui.typewrite(', ')
        elif insert_type == "Semicolon":
            pyautogui.typewrite('; ')
    else:
        if debug_mode: 
            print("Received non-usable return values.")

def main():
    global debug_mode, verbose, separator
    mac_address = None
    simulated_response = None
    insert_type = "Enter"  # Default insertion type

    # Argument parsing
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-mac":
            mac_address = sys.argv[i + 1]  # Get the MAC address from the command line arguments
        elif sys.argv[i] == "-debug":
            debug_mode = True  # Enable debug mode
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                simulated_response = sys.argv[i + 1]  # Get the simulated response
                i += 1  # Increment index to skip the response value
        elif sys.argv[i] == "-post-insert-action":
            if i + 1 < len(sys.argv):
                insert_type = sys.argv[i + 1]  # Set the insertion type
                i += 1  # Increment index to skip the insertion type value
        elif sys.argv[i] == "-verbose":
            verbose = True  # Enable verbose mode
        elif sys.argv[i] == "-separator":
            if i + 1 < len(sys.argv) and sys.argv[i + 1] in ["comma", "point"]:
                separator = sys.argv[i + 1]  # Set the separator
                i += 1  # Increment index to skip the separator value

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mac_file_path = os.path.join(script_dir, "bosch-bluetoothmac.txt")

    if not mac_address:
        if os.path.exists(mac_file_path):
            with open(mac_file_path, "r") as f:
                mac_address = f.read().strip()  # Read MAC address from file
            print(f"Using Bluetooth MAC: {mac_address}")
        else:
            mac_address = input("Please enter the Bluetooth MAC address: ")
            print("The Bluetooth MAC can often be found in the settings under 'Information' of the laser distance meter.")

    if simulated_response:
        print("Debug mode - a return value was provided:", simulated_response)
        print_response(simulated_response, insert_type)  # Process the simulated response
        sys.exit()  # Exit the program

    device = connect_to_laser(mac_address)  # Connect to the laser device

    # Set the delegate for the laser with insert_type
    device.setDelegate(LaserDelegate(insert_type))

    # Activate measurement
    write_characteristic(device, 0x001e, "c0550201001a")  # Handle for 0x001e
    write_characteristic(device, 0x001f, "0200")  # Handle for 0x001f

    # Main loop to wait for indications
    while True:
        if device.waitForNotifications(1.0):  # Wait for notifications
            continue

if __name__ == "__main__":
    main()  # Run the main function
