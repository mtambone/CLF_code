import serial
import time

VXM_COMMAND = 255
VXM_RETURN = 50
VMX_WAIT = 800000

class VXM:

    def __init__(self, port, baudrate = 9600):
        self.port=port
        self.baudrate = baudrate
        self.serial= None

    def read_command(self):   

        if self.serial and self.serial.is_open:
            try:
                response = self.serial.read(VXM_RETURN).decode(errors='ignore').strip()
                return response
            except serial.SerialException: 
                print(f"VXM:READ_R:ERROR:Unable to read response")
                return -1
        return ""

    def send_command(self, command):

        if self.serial and self.serial.is_open:
            try:
                self.serial.flushInput()
                self.serial.write(f"{command}\r".encode())
                time.sleep(0.5)
                self.serial.write(b"y\r")
                time.sleep(0.5)

                response = self.read_response()

                return response

            except serial.SerialException as e:
                print(f"VXM:SEND_COMM:Unable to send {command} command: {e}")
                return -1
        else:
            print(f"VXM:SEND_COMM:Serial port is not open")
            return -1
        
    def flush_buffers(self):

        try:
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            time.sleep(0.1)
            return 0

        
        except Exception as e:
            print(f"VXM:FLUSH_BUFFERS:Unable to flush buffers")
            return -1
    
    def connect(self):

        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=VMX_WAIT)
            
            self.flush_buffers()
            self.send_command("F")
            self.send_command("C")
            self.send_command("V")

            ready = self.read_command()
            if ready == "R": 
                print(f"VXM:CONNECT:Connected to {self.port} at {self.baudrate} baud")
                return 0
            
            else: 
                for i in range(0, 10):
                    ready = self.read_command()
                    print(f"VXM:CONNECT:Attempt {i}, response: {ready}")
                    if ready == "R":
                        print(f"VXM:CONNECT:Connected to {self.port} at {self.baudrate} baud")
                        return 0
                    else:
                        print(f"VXM:CONNECT:ERROR:Unable to reach device at {self.port}. Trying again...")
                        
        except serial.SerialException as e:
            print(f"VXM:CONNECT:ERROR:Unable to reach device at {self.port}: {e}")
            return -2
        

