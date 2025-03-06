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

        ####vxm conf####

        self.stpx = 80
        self.stpy = 80
        self.spdx = 1200
        self.spdy = 1500
        self.lmtx = 28540
        self.lmty = 28498
        #AZIMUTHAL number of steps from limit switch to zero (North)
        #POSX 2902 changed by medina Y15M04D28
        self.POSX = 2974


        #VERTICAL number of step from limit swit to zero (horizontal plane)
        #POSY 8677   modified by Kevin and Carlos on Mar 2017
        self.POSY = 8598


    def read_command(self):   

        if self.serial and self.serial.is_open:
            try:
                response = self.serial.read(VXM_RETURN).decode(errors='ignore').strip()
                response = str(response)
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
                
                print("VXM:CONNECT:ERROR:Maximum number of trial exceeded")
                return -2
                       
        except serial.SerialException as e:
            print(f"VXM:CONNECT:ERROR:Unable to reach device at {self.port}: {e}")
            return -2
        
########prove funzioni#############

    def set_model(self, motor, model):
        
        self.flush_buffers()
        ready = self.send_command(f"setM{motor}M{model},R")
        
        if ready and ready== "^":
            print(f"VXM:SET_MODEL:VXM at {self.port}:Motor {motor} model set: {model}")
            return 0
        else:
            print(f"VXM:SET_MODEL:ERROR:VXM at {self.serial}:ìUnable to set motor {motor} model")
            return -1
      
    def set_acc(self, motor, value):

        self.flush_buffers()
        ready= self.send_command(f"A{motor}M{value},R")
        if ready and ready== "^":
            print(f"VXM:SET_ACC:VXM at {self.port}:Motor {motor} acceleration set: {value}")
            return 0
        else:
            print(f"VXM:SET_ACC:ERROR:VXM at {self.serial}:Unable to set motor {motor} acceleration")
            return -1

    def set_speed(self, motor, value):

        self.flush_buffers()
        ready = self.send_command(f"S{motor}M{value},R")
        if ready and ready== "^":
            print(f"VXM:SET_SPEED:VXM at {self.port}:Motor {motor} speed set: {value}")
            return 0
        else:
            print(f"VXM:SET_SPEED:ERROR:VXM at {self.serial}:Unable to set motor {motor} speed")
            return -1

    def wait(self,dtime):
        wait_time = f"{dtime}0"

        self.flush_buffers()
        self.send_command(f"P{dtime},R")
        time.sleep(wait_time)
        ready = self.read_command()
        if ready and ready== "^":
            print(f"VXM:WAIT:VXM at {self.serial}:Wait ended")
            return 0
        else:
            print(f"VXM:SET_SPEED:ERROR:VXM at {self.serial}:Unable to set waiting")
            return -1
    
    def move_FWD(self, motor, pos):

        self.flush_buffers()
         
        try:
            self.send_command(f"I{motor}M{pos},R")

            while self.read_command() != "^": 
                time.sleep(0.5)

            print(f"VXM:MOVE_FWD:VXM at {self.serial}: motor {motor} in position {pos}")
            return 0 
        
        except Exception as e:
            print(f"VXM:MOVE_FWD:ERROR:VXM at {self.serial}:unable to move motor {motor} in position {pos}")
            return -1
        
    def move_BWD(self, motor, pos):

        self.flush_buffers()
        try:
            self.send_command(f"I{motor}M-{pos},R")

            while self.read_command() != "^": 
                time.sleep(0.5)

            print(f"VXM:MOVE_BWD:VXM at {self.serial}: motor {motor} in position {pos}")
            return 0 
        
        except Exception as e:
            print(f"VXM:MOVE_BWD:ERROR:VXM at {self.serial}:unable to move motor {motor} in position {pos}")
            return -1
           
    def move_Neg0(self, motor):

        self.flush_buffers()
        try:
            self.send_command(f"I{motor}M-0,R")

            while self.read_command() != "^": 
                time.sleep(0.5)

            print(f"VXM:MOVE_NEG0:VXM at {self.serial}: motor {motor} in negative zero position")
            return 0 
        
        except Exception as e:
            print(f"VXM:MOVE_BWD:ERROR:VXM at {self.serial}:unable to move motor {motor} in negative zero position")
            return -1
        
    def move_Pos0(self, motor):

        self.flush_buffers()
        try:
            self.send_command(f"I{motor}M0,R")

            while self.read_command() != "^": 
                time.sleep(0.5)

            print(f"VXM:MOVE_NEG0:VXM at {self.serial}: motor {motor} in positive zero position")
            return 0 
        
        except Exception as e:
            print(f"VXM:MOVE_BWD:ERROR:VXM at {self.serial}:unable to move motor {motor} in positive zero position")
            return -1
            
    def move_ABS(self, motor, abs_pos):

        self.flush_buffers()
        abs_pos = int(abs_pos)

        if motor == 1:
            current_pos = self.send_command("X")
        else:
            current_pos = self.send_command("Y")

        current_pos = int(current_pos)

        if current_pos == abs_pos:

            print(f"VXM:MOVE_ABS:VXM at {self.serial}:motor {motor} already in absolute position {abs_pos}")
        
        else:

            try:
                self.send_command(f"IA{motor}M{abs_pos}")
        
                while self.read_command() != "^": 
                    time.sleep(0.5)

                print(f"VXM:MOVE_ABS:VXM at {self.serial}:motor {motor} in absolute position {abs_pos}")
                return 0 
            
            except Exception as e:
                print(f"VXM:MOVE_ABS:ERROR:VXM at {self.serial}:unable to move motor {motor} in absolute position {abs_pos}")
                return -1

    def set_ABSzero(self, motor, abs_zero):
        
        self.flush_buffers()

        self.move_ABS(motor, abs_zero)

        try:
            self.send_command(f"IA{motor}M-0")
    
            while self.read_command() != "^": 
                time.sleep(0.5)

            print(f"VXM:MOVE_ABS:VXM at {self.serial}: motor {motor} in absolute position {abs_zero}")
            return 0 
        
        except Exception as e:
            print(f"VXM:MOVE_ABS:ERROR:VXM at {self.serial}:unable to move motor {motor} in absolute position {abs_zero}")
            return -1







