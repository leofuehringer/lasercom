# LaserCom

**LaserCom** is a Bluetooth-enabled laser rangefinder application designed to communicate and manage distance measurements efficiently. The application connects to Bluetooth-enabled laser measuring devices and allows users to easily copy measurement results to the clipboard with customizable insertion options. With LaserCom, the laser rangefinder can be used like a connected Bluetooth keyboard, providing each measurement as a keyboard input. This feature simplifies integration into existing workflows and software applications, allowing measurement values to be directly inserted into documents or spreadsheets.

## Features
- **Laser as Bluetooth Keyboard**: With LaserCom, the laser rangefinder can be used like a connected Bluetooth keyboard, providing keyboard input for each measurement.
- **Bluetooth Connectivity**: Seamlessly connect to Bluetooth laser rangefinders.
- **Distance Measurement**: Capture accurate distance measurements.
- **Clipboard Integration**: Automatically copy results to the clipboard.
- **Custom Insertion Options**: Choose how measurements are inserted (e.g., Enter, Tab, Comma, Semicolon).
- **Debug Mode**: Optional debug mode for troubleshooting and development.

## Tested Devices

This application has been tested with the following laser rangefinder:

- **Bosch GLM 50-27 GC**: A reliable and precise laser distance meter that connects via Bluetooth. The application successfully communicates with this device, allowing for accurate distance measurements and data retrieval.

Additionally, other new Bosch laser rangefinders that adhere to the same standard should also work with LaserCom. Older laser measuring devices may function with minor adjustments; however, the return values will need to be evaluated differently. 

For more information, you can refer to this [EEVblog forum post](https://www.eevblog.com/forum/projects/hacking-the-bosch-glm-20-laser-measuring-tape/).
If you have tested this application with other devices, please feel free to contribute by adding your findings!

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

Here’s an additional section for your `README.md` file that covers the technical implementation details, including the connection setup with `bluepy`, testing with `gatttool`, and how to interpret the measurement results:


## Technical Implementation

### Connection Setup with Bluepy

The application uses the `bluepy` library to establish a connection with Bluetooth-enabled laser rangefinders. To test the connection and communicate with the device, you can also use `gatttool`, which is a command-line utility for interacting with Bluetooth Low Energy (BLE) devices.

#### Using Gatttool for Testing

1. Open your terminal and run the following command to start `gatttool` in interactive mode, replacing the MAC address with your device's MAC address:
   ```bash
   gatttool -b 40:79:12:9A:E3:88 -I
   ```

2. Once in interactive mode, connect to the device:
   ```bash
   connect
   ```

3. To start a measurement, you can send the following command to activate the laser:
   ```bash
   char-write-req 0x001e c05601001e
   ```
   This command must be executed twice: the first time to activate the laser and the second time to initiate the measurement. This simulates pressing the laser button manually.

4. After initiating the measurement, you can request data from the laser using:
   ```bash
   char-write-req 0x001f 0200
   char-write-req 0x001e c0550201001a
   ```

### Receiving Measurement Values

When you successfully receive data from the laser, it will be in a hex format. The response structure typically starts with a specific header followed by the measurement data.

#### Understanding the Hexadecimal Response

The hex values returned by the laser can be interpreted as follows:

- The first few bytes of the response indicate the command and status.
- The measurement data is usually found in specific positions within the hex string.

For example, if you receive a hex response like `c055100606007a0094f6463e`, the measurement data can be extracted from the relevant bytes.

#### Converting Hexadecimal to Decimal

To convert the measurement hex value to a decimal number, you can use the following steps:

1. Extract the relevant hex portion (e.g., `007a`).
2. Convert the hex value to an unsigned integer using Python or an online calculator.
3. Use the following Python function to convert the hex value to a float:
   ```python
   def hex_to_float(hex_value):
       unsigned_int = int(hex_value, 16)  # Convert hex to unsigned integer
       packed = struct.pack('I', unsigned_int)  # Pack the integer into bytes
       float_converted = struct.unpack('f', packed)[0]  # Unpack bytes as a float
       return float_converted
   ```

4. Multiply the resulting float by 100 to convert it to centimeters.

For online conversion, you can use tools like:
- [RapidTables Hex to Decimal Converter](https://www.rapidtables.com/convert/number/hex-to-decimal.html)
- [Unit Conversion Calculator](https://www.unitconverters.net/)

This section provides a comprehensive overview of how to set up the connection, send commands, and interpret the measurement results from the laser rangefinder.

### Summary of the Section
- **Connection Setup**: Instructions for using `bluepy` and `gatttool`.
- **Testing with Gatttool**: Detailed steps to connect and send commands to the laser device.
- **Receiving Measurement Values**: Explanation of how to interpret the hex response.
- **Converting Hexadecimal to Decimal**: Steps and code for converting hex values to decimal, including references to online calculators.
