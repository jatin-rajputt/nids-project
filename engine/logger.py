import datetime
import os
from core.config import LOG_FILE

def log_alert(message):
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%D %H;%M;%S")
    
    log_entry = f"[{timestamp}] {message}"
    
    os.makedirs("data", exist_ok = True)
    
    with open(LOG_FILE, "a")as file:
        file.write(log_entry +"\n")
        
    return log_entry