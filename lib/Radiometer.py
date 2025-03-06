import serial
import time

RADIOMETER_RETURN = 255
RADIOMETER_WAIT = 500000 

class Rad_Monitor_3700:

    def __init__(self, port, baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):

        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout = RADIOMETER_WAIT)
            print(f"RADM_MON_3700:CONN:Connected to {self.port} at {self.baudrate} baud")
            return 0       
        except serial.SerialException as e:
            print(f"RADM_MON_3700:Unable to reach the device {self.port}: {e}") 
            return -2
        
    def flush_buffers(self):

        try:
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            time.sleep(0.1)

        except Exception as e:
            print(f"RADM_MON_3700:FLUSH_BUFFERS:Unable to flush buffers")
            return -1
        
    def read_command(self):

        if self.serial and self.serial.is_open:
            try:
                response = self.serial.read(RADIOMETER_RETURN).decode(errors='ignore')
                response = str(response)
                return response
            except serial.SerialException:
                print("RADM_MON_3700:ERROR:Unable to read response")

    def send_command(self, command):

            if self.serial and self.serial.is_open:
                try:
                    self.flush_buffers()
                    self.serial.write(f"{command}\r".encode())
                    time.sleep(0.5)
                    self.serial.write(b"y\r")
                    time.sleep(0.5)

                    response = self.read_command()

                    return response

                except serial.SerialException as e:
                    print(f"RADM_MON_3700:SEND_COMM:Unable to send {command} command: {e}")
                    return -1   
            else:
                print(f"RADM_MON_3700:SEND_COMM:Serial port is not open")
                return -1
            
    def set_parameter(self, parameter, value):

        parameter_set = self.send_command(f"{parameter} {value}")

        if parameter_set:
            preturn = parameter_set.split()

            if preturn == 2 and preturn[0] == f"{parameter}":
                print(f"RADM_MON_3700:PARAMETER_SET:Parameter {preturn[0]}, value set: {preturn[1]}")
                return preturn
            else:
                print(f"RADM_MON_3700:PARAMETER_SET:ERROR:Unable to set parameter {preturn[0]}")
                return -1

    def check_parameter(self, parameter):

        parameter_check = self.send_command(f"{parameter} ?")

        if parameter_check:
            preturn = parameter_check.split()

            if preturn == 2 and preturn[0] == f"{parameter}":
                print(f"RADM_MON_3700:PARAMETER_CHECK:Parameter {preturn[0]}, value checked: {preturn[1]}")
                return preturn[1]
            else:
                print(f"RADM_MON_3700:PARAMETER_CHECK:ERROR:Unable to check parameter {preturn[0]}")
                return -1

    def rad_info(self):

        self.flush_buffers()

        try:
            id = self.send_command("ID")
            vers = self.send_command("VR")
            probe = self.send_command("PA")
            status = self.send_command("ST")
            if id and vers and probe and status:
                print(f"RADM_MON_3700:RAD_INFO:Radiometer identity: {id}")
                print(f"RADM_MON_3700:RAD_INFO:Radiometer version: {vers}")
                print(f"RADM_MON_3700:RAD_INFO:Probe id and type: {probe}")
                print(f"RADM_MON_3700:RAD_INFO:Status: {status}")

        except Exception as e:
            print(f"RADM_MON_3700:RAD_INFO:ERROR:Some problem occurred: {e}")

    def rad_set(self):

        try:
            self.flush_buffers()

            self.set_parameter("TG", 3)
            self.set_parameter("SS", 0)
            self.set_parameter("FA", 1.00)
            self.set_parameter("EV", 1)
            self.set_parameter("BS", 0)
            self.set_parameter("RA", 2)
            self.send_command("AD")

        except Exception as e:
            print(f"RADM_MON_3700:SET_UP:ERROR:Some problem occurred: {e}")

    def set_range(self, range):

        self.flush_buffers()
        self.set_parameter("RA", range)
        

class Rad_Ophir:

    def __init___(self, port, baudrate = 9600):

        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):

        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout = RADIOMETER_WAIT)
            print(f"RADM_OPHIR:CONN:Connected to {self.port} at {self.baudrate} baud")
            return 0       
        except serial.SerialException as e:
            print(f"RADM_OPHIR:Unable to reach the device {self.port}: {e}") 
            return -2
        
    def flush_buffers(self):

        try:
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            time.sleep(0.1)

        except Exception as e:
            print(f"RADM_OPHIR:FLUSH_BUFFERS:Unable to flush buffers")
            return -1
        
    def read_command(self):

        if self.serial and self.serial.is_open:
            try:
                response = self.serial.read(RADIOMETER_RETURN).decode(errors='ignore')
                return response
            except serial.SerialException:
                print("RADM_OPHIR:ERROR:Unable to read response")
                return -1

    def send_command(self, command):

            if self.serial and self.serial.is_open:
                try:
                    self.flush_buffers()
                    self.serial.write(f"{command}\r".encode())
                    time.sleep(0.5)
                    self.serial.write(b"y\r")
                    time.sleep(0.5)
                    

                    response = self.read_command()

                    return response

                except serial.SerialException as e:
                    print(f"RADM_OPHIR:SEND_COMM:Unable to send {command} command: {e}")
                    return -1   
            else:
                print(f"RADM_OPHIR:SEND_COMM:Serial port is not open")
                return -1
            
    def set_parameter(self, parameter, value):

        parameter_set = self.send_command(f"{parameter} {value}")

        if parameter_set:
            preturn = parameter_set.split()

            if preturn == 2 and preturn[0] == f"{parameter}":
                print(f"RADM_OPHIR:PARAMETER_SET:Parameter {preturn[0]}, value set: {preturn[1]}")
                return preturn
            else:
                print(f"RRADM_OPHIR:PARAMETER_SET:ERROR:Unable to set parameter {preturn[0]}")
                return -1

    def check_parameter(self, parameter):

        parameter_check = self.send_command(f"{parameter} ?")

        if parameter_check:
            preturn = parameter_check.split()

            if preturn == 2 and preturn[0] == f"{parameter}":
                print(f"RADM_OPHIR:PARAMETER_CHECK:Parameter {preturn[0]}, value checked: {preturn[1]}")
                return preturn[1]
            else:
                print(f"RADM_OPHIR:PARAMETER_CHECK:ERROR:Unable to check parameter {preturn[0]}")
                return -1

    def rad_info(self):
        self.flush_buffers()
        try: 
            id = self.send_command("$II")
            probe = self.send_command("$HI")
            battery = self.send_command("$BC")

            if id and probe and battery:
                print(f"RADM_OPHIR:RAD_INFO:Radiometer identity: {id}")                
                print(f"RADM_OPHIR:RAD_INFO:Probe id and type: {probe}")
                print(f"RADM_OPHIR:RAD_INFO:Battery conditions: {battery}")

                return 0

            else:
                missing = []
                if not id:
                    missing.append("id")

                if not probe:
                    missing.append("probe")

                if not battery:
                    missing.append("battery")
                print(f"RAD_OPHIR_RAD_INFO:ERROR:Unable to retrieve info: {missing}")
            
        except Exception as e:
            print(f"RAD_OPHIR:RAD_INFO:ERROR:Some problem occurred: {e}")
            return -1

            


    def rad_set(self):

        self.flush_buffers()
        self.set_parameter("$DU", 1)
    



