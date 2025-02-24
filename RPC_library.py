import serial
import time

# Costanti
RPC_RETURN = 50
RPC_WAIT = 1  # Timeout in secondi

# Stati degli outlet
RPC_BREAKER = 0
RPC_RAMAN = 1
RPC_RAD = 2
RPC_LSR = 3
RPC_RCOVER = 4
RPC_VCOVER = 5
RPC_VXM = 6

class RPCDevice:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.status = [-1] * 7  # Stato iniziale sconosciuto

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=RPC_WAIT)
            print(f"RPC:CONN: Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"RPC:CONN: Unable to open device {self.port}: {e}")

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            self.serial.flushInput()
            self.serial.write(f"{command}\r".encode())
            time.sleep(0.5)
            self.serial.write(b"y\r")  # Conferma comando
            time.sleep(0.3)
        else:
            print("RPC:SEND_COMM:Serial port is not open.")

    def read_response(self):
        if self.serial and self.serial.is_open:
            response = self.serial.read(RPC_RETURN).decode(errors='ignore').strip()
            return response
        return ""

    def rpc_on(self, outlet):
        for _ in range(3):
            self.send_command(f"on {outlet}")
        if self.rpc_status(outlet) == 1:
            return 1
        for _ in range(4):
            self.send_command(f"on {outlet}")
        if self.rpc_status(outlet) == 1:
            return 1
        print(f"RPC:ON:ERROR:Outlet {outlet} did not turn ON.")
        return 0

    def rpc_off(self, outlet):
        for _ in range(3):
            self.send_command(f"off {outlet}")
        if self.rpc_status(outlet) == 0:
            return 0
        for _ in range(4):
            self.send_command(f"off {outlet}")
        if self.rpc_status(outlet) == 0:
            return 0
        print(f"RPC:OFF:ERROR:Outlet {outlet} did not turn OFF.")
        return 1

    def rpc_status(self, outlet):
        self.serial.flushInput()
        self.serial.write(b"\r")
        time.sleep(0.05)

        response = self.read_response()
        if "Circuit Breaker: Off" in response:
            self.status[RPC_BREAKER] = 0
            return -2
        if "Circuit Breaker: On" in response:
            self.status[RPC_BREAKER] = 1

        outlet_status = {
            "1)...ramansys  : On": RPC_RAMAN,
            "2)...rad (mon) : On": RPC_RAD,
            "3)...laser     : On": RPC_LSR,
            "4)...rmotor    : On": RPC_RCOVER,
            "5)...Vcover    : On": RPC_VCOVER,
            "6)...vxm       : On": RPC_VXM
        }

        outlet_off_status = {
            "1)...ramansys  : Off": RPC_RAMAN,
            "2)...rad (mon) : Off": RPC_RAD,
            "3)...laser     : Off": RPC_LSR,
            "4)...rmotor    : Off": RPC_RCOVER,
            "5)...Vcover    : Off": RPC_VCOVER,
            "6)...vxm       : Off": RPC_VXM
        }

        for line in response.split('\n'):
            for key, val in outlet_status.items():
                if key in line:
                    self.status[val] = 1
            for key, val in outlet_off_status.items():
                if key in line:
                    self.status[val] = 0

        if outlet >= 0 and outlet <= 6:
            return self.status[outlet]
        elif outlet == 0:
            return sum(1 for s in self.status if s == 1)
        else:
            return -1

if __name__ == "__main__":
    rpc = RPCDevice('/dev/ttyUSB0')  # Modifica la porta se necessario
    rpc.connect()
    
    outlet = 1  # Cambia l'outlet da controllare
    print(f"Accensione outlet {outlet}:", rpc.rpc_on(outlet))
    print(f"Stato outlet {outlet}:", rpc.rpc_status(outlet))
    print(f"Spegnimento outlet {outlet}:", rpc.rpc_off(outlet))
    print(f"Stato outlet {outlet}:", rpc.rpc_status(outlet))
