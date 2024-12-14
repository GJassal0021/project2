# Project 2 Client/Server

# Student Name: Gurleen Kaur Jassal
# Student ID: 100942372
# Submission Date : 13 December 2024
# Instructor - Philip J

# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

# The Server

import socket  # For network communication
import json  # For JSON parsing
import time  # For time-related functions
import PySimpleGUI as sg  # For creating the GUI

class ServerGUI:
    def __init__(self):
        """Initialize the server GUI."""
        sg.theme('DarkBlue')  # Set the GUI theme
        
        # Define the layout of the GUI
        layout = [
            [sg.Text('🔴', key='-LED-', font=('Arial', 20), text_color='red')],  # LED indicator
            *[[sg.Text(f"{field}: N/A", key=f'-{field}-', text_color='white', background_color='#283b5b')] for field in ["Temp", "Volts", "Memory usage", "Clock Speed", "CPU Usage", "Clock Frequency", "Iteration"]],  # Data fields
            [sg.Button('Exit', button_color=('white', '#FF5733'))]  # Exit button with custom colors
        ]
        
        # Create the window
        self.window = sg.Window('Server Data Display', layout, finalize=True)
        self.led_state = False  # Initialize LED state

    def update_data(self, data):
        """Update the GUI with new data."""
        for field, value in data.items():
            self.window[f'-{field}-'].update(f"{field}: {value}")  # Update each field with new data
        
        # Toggle LED state
        self.led_state = not self.led_state
        self.window['-LED-'].update("⚫" if self.led_state else "🔴")  # Update LED display

    def run(self):
        """Run the GUI event loop."""
        sock = socket.socket()  # Create a socket object
        port = 1500  # Set the port for the server
        sock.bind(('', port))  # Bind to the port
        sock.listen(5)  # Listen for connections

        print('Socket is listening...')
        c, addr = sock.accept()  # Accept a connection
        

        while True:
            event, values = self.window.read(timeout=100)  # Read GUI events
            if event == sg.WINDOW_CLOSED or event == 'Exit':  # Check for exit conditions
                break

            try:
                json_received = c.recv(1024)  # Receive data from the client
                if json_received:
                    data = json.loads(json_received)  # Parse the JSON data
                    self.update_data(data)  # Update the GUI with new data
            except Exception:
                print(f"Error")  # Print any errors
                break

        self.window.close()  # Close the GUI window
        c.close()  # Close the client connection

def main():
    """Main function to handle server operations."""
    gui = ServerGUI()  # Create a ServerGUI instance
    gui.run()  # Run the GUI

if __name__ == "__main__":
    try:
        main()  # Run the main function
    except KeyboardInterrupt:
        print("Exiting gracefully...")  # Handle keyboard interrupt
