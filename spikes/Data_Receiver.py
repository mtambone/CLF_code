import serial
import csv
import os

# Configura la porta seriale
PORT = "/dev/data0"  # Sostituisci con la tua porta seriale
HEADER = 'BAAB'
FOOTER = 'FEEF'
PACKET_SIZE = 40  # 4 byte di header + 12 byte di dati + 4 byte di footer
CSV_FILE = "dati_seriale.csv"

# Controlla se il file esiste per scrivere l'intestazione solo una volta
file_exists = os.path.exists(CSV_FILE)

def read_serial():
    with serial.Serial(PORT, 115200, timeout=1) as ser, open(CSV_FILE, mode='a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Scrive l'intestazione se il file è nuovo
        if not file_exists:
            csv_writer.writerow(["unix time", "time_ns", "width_ns"])
        
        buffer = b""
        while True:
            buffer += ser.read(PACKET_SIZE)  # Legge il pacchetto intero
            
            # Cerca l'header
            start_idx = buffer.find(HEADER.encode())
            if start_idx != -1 and len(buffer) >= start_idx + PACKET_SIZE:
                packet = buffer[start_idx:start_idx + PACKET_SIZE]
                buffer = buffer[start_idx + PACKET_SIZE:]  # Rimuove il pacchetto letto
                #print(packet[-5:-1])
                # Verifica il footer
                if packet[-5:-1] == FOOTER.encode():
                    data = packet[5:-5]  # Estrai solo i dati centrali
                    #print(data.decode().split('\r'))
                    # Converti i 3 numeri in interi a 32 bit (big endian)
                    values = data.decode().split('\r')[:-1]#[int.from_bytes(data[i:i+4], 'big') for i in range(0, 30, 5)]
                    seconds=(int(values[0],16)<<16)+int(values[1],16)
                    counter=(int(values[2],16)<<16)+int(values[3],16)*10
                    lenght=(int(values[4],16)<<16)+int(values[5],16)*10
                    #print(seconds, counter, lenght)
                    # Stampa i dati a schermo
                    #print(f"Dati ricevuti: {values}")
                    values=[seconds, counter,lenght]
                    # Scrive i dati nel file CSV
                    csv_writer.writerow(values)
                    csvfile.flush()  # Assicura che i dati vengano scritti subito
                else:
                    print("Errore: pacchetto non valido!")

if __name__ == "__main__":
    read_serial()

