import serial
import csv
import os

# Configura la porta seriale
PORT = "/dev/data0"  # Sostituisci con la tua porta seriale
HEADER = 'BAAB'
FOOTER = 'FEEF'
PACKET_SIZE = 16  # 4 byte di header + 12 byte di dati + 4 byte di footer
CSV_FILE = "dati_seriale.csv"

# Controlla se il file esiste per scrivere l'intestazione solo una volta
file_exists = os.path.exists(CSV_FILE)

def read_serial():
    with serial.Serial(PORT, 115200, timeout=1) as ser, open(CSV_FILE, mode='a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Scrive l'intestazione se il file è nuovo
        if not file_exists:
            csv_writer.writerow(["Valore 1", "Valore 2", "Valore 3"])
        
        buffer = b""
        while True:
            buffer += ser.read(PACKET_SIZE)  # Legge il pacchetto intero
            
            # Cerca l'header
            start_idx = buffer.find(HEADER)
            if start_idx != -1 and len(buffer) >= start_idx + PACKET_SIZE:
                packet = buffer[start_idx:start_idx + PACKET_SIZE]
                buffer = buffer[start_idx + PACKET_SIZE:]  # Rimuove il pacchetto letto
                
                # Verifica il footer
                if packet[-4:] == FOOTER:
                    data = packet[4:-4]  # Estrai solo i dati centrali

                    # Converti i 3 numeri in interi a 32 bit (big endian)
                    values = [int.from_bytes(data[i:i+4], 'big') for i in range(0, 12, 4)]
                    
                    # Stampa i dati a schermo
                    print(f"Dati ricevuti: {values}")
                    
                    # Scrive i dati nel file CSV
                    csv_writer.writerow(values)
                    csvfile.flush()  # Assicura che i dati vengano scritti subito
                else:
                    print("Errore: pacchetto non valido!")

if __name__ == "__main__":
    read_serial()

