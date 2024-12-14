# Project 2 Client/Server

# Student name: Gurleen Kaur Jassal
# Student ID: 100942372
# Submission Date : 13 December 2024
# Instructor - Philip J

# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

# The client

import socket  # For network communication
import sys  # For system-specific parameters and functions
import json  # For JSON encoding and decoding
import time  # For time-related functions
import os  # For interacting with the operating system
from pathlib import Path  # For handling file paths
import PySimpleGUI as sg  # For creating GUI

IS_RPI = Path("/etc/rpi-issue").exists()  # Check if running on Raspberry Pi

if not IS_RPI:  # If not running on Raspberry Pi
    print("This script can only run on a Raspberry Pi.")  # Print error message
    sys.exit(0)  # Exit the script

print("Correct Hardware")  # Confirm correct hardware

def get_core_temperature():
    """Retrieve the core temperature from the Raspberry Pi."""
    temp = os.popen('vcgencmd measure_temp').readline()  # Execute command and read output
    return round(float(temp.split('=')[1].split("'")[0]), 1)  # Parse and return temperature

def get_voltage():
    """Retrieve the voltage from the Raspberry Pi."""
    voltage = os.popen('vcgencmd measure_volts').readline()  # Execute command and read output
    return round(float(voltage.split('=')[1].split('V')[0]), 1)  # Parse and return voltage

def get_memory_usage():
    """Retrieve memory usage from the Raspberry Pi."""
    mem_info = os.popen('vcgencmd get_mem arm').readline()  # Execute command and read output
    return int(mem_info.split('=')[1].split('M')[0])  # Parse and return memory usage

def get_clock_speed():
    """Retrieve clock speed from the Raspberry Pi."""
    clock_speed = os.popen('vcgencmd measure_clock arm').readline()  # Execute command and read output
    return int(clock_speed.split('=')[1])  # Parse and return clock speed

def get_cpu_usage():
    """Retrieve CPU usage from the Raspberry Pi."""
    return round(float(os.popen('top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk \'{print 100 - $1}\'').readline()), 1)  # Execute complex command, parse output

def collect_data(iteration):
    """Collect all necessary data into a dictionary."""
    return {  # Return dictionary with all collected data
        "Temp": get_core_temperature(),
        "Volts": get_voltage(),
        "Memory usage": get_memory_usage(),
        "Clock Speed": get_clock_speed(),
        "CPU Usage": get_cpu_usage(),
        "Clock Frequency": get_clock_speed(),
        "Iteration": iteration
    }

def main():
    """Main function to handle client operations."""
    sg.theme('DarkBlue')  # Set GUI theme

    layout = [  # Define GUI layout
        [sg.Text('🔴', key='-LED-', font=('Arial', 20))],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Client Connection Status', layout, finalize=True)  # Create GUI window

    sock = socket.socket()  # Create a socket object
    port = 1500  # Define port number
    address = "10.102.13.206"  # Define server address

    try:
        sock.connect((address, port))  # Attempt to connect to server
        
        for i in range(50):  # Loop 50 times
            event, values = window.read(timeout=10)  # Read GUI events
            if event == sg.WINDOW_CLOSED or event == 'Exit':  # Check for exit conditions
                break

            data = collect_data(i)  # Collect data
            json_result = json.dumps(data)  # Convert data to JSON
            sock.send(json_result.encode())  # Send JSON data to server
            
            window['-LED-'].update("⚫" if i % 2 else "🔴")  # Toggle LED indicator
            
            time.sleep(2)  # Wait for 2 seconds

    except socket.error:  # Handle socket errors
        print("Socket error")
    
    finally:
        sock.close()  # Close the socket
        print("Connection closed")  # Print closure message
        window.close()  # Close the GUI window

if __name__ == "__main__":
    main()  # Run the main function if script is executed directly
