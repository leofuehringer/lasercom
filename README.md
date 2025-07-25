# LaserCom

**LaserCom** is a Bluetooth-enabled laser rangefinder application designed for capturing and managing distance measurements efficiently. The application connects to Bluetooth-enabled laser measuring devices and allows users to easily copy measurement results to the clipboard with customizable insertion options.

## Features

- **Bluetooth Connectivity**: Seamlessly connect to Bluetooth laser rangefinders.
- **Distance Measurement**: Capture accurate distance measurements.
- **Clipboard Integration**: Automatically copy results to the clipboard.
- **Custom Insertion Options**: Choose how measurements are inserted (e.g., Enter, Tab, Comma, Semicolon).
- **Debug Mode**: Optional debug mode for troubleshooting and development.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LaserCom.git
   cd LaserCom
   ```
1. Clone the repository:
   ```bash
   pip install bluepy pyperclip pyautogui
   ```



## Usage
To run the application, use the following command:
```bash
  python lasercom.py -mac <MAC_ADDRESS> [-s <insert_option>] [-debug]
  ```
Replace <MAC_ADDRESS> with the Bluetooth MAC address of your laser rangefinder.
Use -s to specify the insertion option (Enter, Tab, Comma, Semicolon).
Use -debug to enable debug mode and pass a simulated response.

## Example
  ```bash
  python lasercom.py -mac 40:79:12:9A:E3:88 -s semicolon
  ```
  
## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
bluepy for Bluetooth Low Energy communication.
pyperclip for clipboard functionality.
pyautogui for simulating keyboard inputs.

Kopieren
You can copy this entire block into your `README.md` file. Just remember to replace `yourusername` with your actual GitHub username. Let me know if you need any more help!
