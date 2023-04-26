from create import hit_point
from time import sleep
import time
from datetime import datetime
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import connect as con

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

print("Aproxime o cartao da leitora...")

while True:
    lcd.write_string(datetime.now().strftime('%b %d  %H:%M:%S\n'))
    sleep(0.95)

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
            lcd.write_string(f"{result[0]} registrou")
            time.sleep(5)
            lcd.clear()
        else:
            lcd.write_string("Tag RFID nao permitida!")
            time.sleep(5)
            
    except:
        sleep(1)