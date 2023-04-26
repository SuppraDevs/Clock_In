from create import hit_point
import time
from datetime import datetime
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import connect as con
import threading

leitorRfid = SimpleMFRC522()

# Raspberry Pi pin setup
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=18, pins_data=[16, 11, 12, 15])
lcd.clear()

sql = "SELECT rfID FROM students"
con.cursor.execute(sql)
result = con.cursor.fetchall()
list_id = []

for i in result:
    list_id.append(*i)

def display_time():
    while True:
        lcd.write_string(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        time.sleep(0.95)

def read_rfid():
    while True:
        try:
            id = leitorRfid.read_id()
            print("ID do aluno: ", id)
            lcd.clear()

            if str(id) in list_id:
                print(id)
                sql = f"SELECT nameStudent FROM students WHERE rfID = '{id}'"
                con.cursor.execute(sql)
                result = con.cursor.fetchone()

                hit_point(id)
                lcd.write_string("Registro aceito!")
                time.sleep(5)
                lcd.clear()
            else:
                lcd.write_string("Tag RFID nao permitida!")
                time.sleep(5)
            
        except:
            time.sleep(1)

thread_time = threading.Thread(target=display_time)
thread_rfid = threading.Thread(target=read_rfid)

thread_time.start()
thread_rfid.start()
