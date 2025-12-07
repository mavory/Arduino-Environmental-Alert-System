import serial
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
# Poznámka: smtplib, MIMEText se importují až ve funkci.

# --- SETTINGS ---
PORT = "COM3"
RATE = 9600
MAIL_FROM = "EMAIL!!!"
APP_PASS = "GOOGLE CODE!!!" # Zabezpečené heslo aplikace

# --- TARGETS & FILES ---
MAIL_TO = "EMAIL!!!!"
CSV_FILE = "data.csv"
H_GRAPH = "humid_graph.png"
T_GRAPH = "temp_graph.png"

# --- LIMITS ---
H_min = 30.0
H_max = 70.0
T_min = 15.0
T_max = 30.0

# state: 1=OK, 0=OUT_OF_LIMIT
H_state = 1
T_state = 1

def send_report(subject, body_html, attachments=None):
    
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEMultipart('related') 
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO
    
    msg.attach(MIMEText(body_html, 'html'))

    # Poznámka: Prilohy se posilaji pouze pri alarmech/navratu
    if attachments:
        for attachment_path in attachments:
            if not os.path.exists(attachment_path):
                print(f"ERROR: Attachment file not found: {attachment_path}")
                continue
            
            with open(attachment_path, 'rb') as f:
                img = MIMEImage(f.read())
                
            img.add_header('Content-ID', f'<{os.path.basename(attachment_path)}>')
            msg.attach(img)


    try:
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.login(MAIL_FROM, APP_PASS)
        s.send_message(msg)
        s.quit()
        print("INFO: Email OK.")
    except Exception as e:
        print(f"ERROR: Email failed: {e}")

def get_data(line):
    
    try:
        line = line.strip()
        
        if "H:" in line and "T:" in line:
            
            # jednodussi parsovani, vice chybove (pozn.: lidska chyba)
            parts = line.split(" ") 
            
            hum = float(parts[0].replace("H:", ""))
            temp = float(parts[1].replace("T:", ""))

            return hum, temp

        if "ERROR" in line:
            print("ERROR: Sensor reported an issue.")
            return None

    except Exception as e:
        print(f"ERROR: Parsing error on line '{line}': {e}")
        
    return None

def check_limits(humidity, temperature):
    global H_state, T_state

    # Priprava tela zprava (HTML) a casu udalosti
    event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # HTML s inline obrazky
    body_template = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px;">
        <h2 style="color: #333;">Monitoring Report</h2>
        <ul style="list-style-type: none; padding: 0;">
            <li style="margin-bottom: 5px;"><b>EVENT TIME:</b> {event_time}</li>
            <li style="margin-bottom: 5px;"><b>Current Humidity:</b> {humidity:.1f}% (Limit: {H_min}% - {H_max}%)</li>
            <li style="margin-bottom: 10px;"><b>Current Temperature:</b> {temperature:.1f}&#8451; (Limit: {T_min}&#8451; - {T_max}&#8451;)</li>
            <li><b>Status:</b> {{status}}</li>
        </ul>
        <hr>
        
        <h3 style="color: #555;">Recent Data Overview:</h3>
        <p><b>Humidity:</b></p>
        <img src="cid:{H_GRAPH}" alt="Humidity Graph">
        <p><b>Temperature:</b></p>
        <img src="cid:{T_GRAPH}" alt="Temperature Graph">
        
    </body>
    </html>
    """
    
    attachments = [H_GRAPH, T_GRAPH]


    # 1. Humidity Check
    if humidity < H_min or humidity > H_max:
        if H_state != 0:
            H_state = 0
            
            # ALARM
            subject = "ALARM: Humidity Out of Range!"
            body = body_template.replace("{{status}}", '<span style="color:red; font-weight:bold;">HUMIDITY OUT OF LIMIT</span>')
            send_report(subject, body, attachments) # Poslat s prilohou
            
    elif H_state != 1:
        H_state = 1
        
        # RETURN TO NORMAL
        subject = "INFO: Humidity Back to Normal"
        body = body_template.replace("{{status}}", '<span style="color:green; font-weight:bold;">All within normal range</span>')
        send_report(subject, body, attachments) # Poslat s prilohou
        
        
    # 2. Temperature Check
    if temperature < T_min or temperature > T_max:
        if T_state != 0:
            T_state = 0
            
            # ALARM
            subject = "ALARM: Temperature Out of Range!"
            body = body_template.replace("{{status}}", '<span style="color:red; font-weight:bold;">TEMPERATURE OUT OF LIMIT</span>')
            send_report(subject, body, attachments) # Poslat s prilohou
            
    elif T_state != 1:
        T_state = 1
        
        # RETURN TO NORMAL
        subject = "INFO: Temperature Back to Normal"
        body = body_template.replace("{{status}}", '<span style="color:green; font-weight:bold;">All within normal range</span>')
        send_report(subject, body, attachments) # Poslat s prilohou


def csv_write(h, t):
    
    now = datetime.now()
    try:
        with open(CSV_FILE, mode='a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), h, t])
    except Exception as e:
        print(f"ERROR: CSV write failed: {e}")

def graph_make():
    try:
        # Poznámka: Jde o rychlou a ne moc cistou implementaci Pandas/Matplotlib
        df = pd.read_csv(CSV_FILE, header=None, names=["time", "H", "T"], parse_dates=["time"])
        
        # H graph
        plt.figure(figsize=(7, 3.5)) 
        plt.plot(df["time"], df["H"])
        plt.title("H Humidity")
        plt.grid(True)
        plt.savefig(H_GRAPH)
        plt.close()
        
        # T graph
        plt.figure(figsize=(7, 3.5))
        plt.plot(df["time"], df["T"], color='red')
        plt.title("T Temperature")
        plt.grid(True)
        plt.savefig(T_GRAPH)
        plt.close()
        
    except Exception as e:
        # Tiskne se pouze pri skutecne chybe, ne pri startu (prazdny soubor)
        if "No columns to parse" not in str(e) and not os.path.exists(CSV_FILE):
            print(f"ERROR: Graphs failed: {e}")


# --- MAIN CODE ---
if __name__ == '__main__':

    try:
        # Ujisti se, ze soubor pro data existuje
        with open(CSV_FILE, 'a'):
            pass
        
        # Start message - BEZ PŘÍLOHY (jak bylo požadováno)
        start_body = f"""
        <html><body style="font-family: Arial, sans-serif;">
            <p>The monitoring script started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.</p>
        </body></html>
        """
        send_report("INFO: Script Started", start_body, attachments=None)

        ser = serial.Serial(PORT, RATE, timeout=1)
        print(f"START: Listening on {PORT}...")
        time.sleep(2) 

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                print(f"Received: {line}")

                measurement = get_data(line)

                if measurement is not None:
                    h, t = measurement
                    csv_write(h, t) 
                    graph_make() 
                    check_limits(h, t) 

            time.sleep(2) 

    except serial.SerialException as e:
        print(f"CRITICAL ERROR: Cannot open port {PORT}: {e}")
    except KeyboardInterrupt:
        print("\nEND: Stopped by user.")