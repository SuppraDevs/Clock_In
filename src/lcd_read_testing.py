from create import hit_point

import time
from datetime import datetime
from time import sleep, mktime
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

leitorRfid = SimpleMFRC522()

# Raspberry Pi pin setup
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=18, pins_data=[16, 11, 12, 15])
loop == False
lcd.clear()
print("Aproxime o cartao da leitora...")

def timer():
    while loop==False:
        lcd.write_string(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        sleep(0.95)

try:
    timer()
    id, ra = leitorRfid.read()
    print("ID do aluno: ", id)
    lcd.clear()

    if id == 383529815217:
        hit_point(id)
        lcd.write_string("Tag RFID válida")
        time.sleep(5)
    else:
        lcd.write_string("Tag RFID nao permitida!")
        time.sleep(5)

finally:
    GPIO.cleanup()


# while loop == True:
#     # # dti = mktime(datetime.now().timetuple())
#     # # ndti = mktime(datetime.now().timetuple())
#     # # if dti < ndti:
#     # #     dti = ndti
#     # #     lcd.clear()
#     # #     lcd.write_string(datetime.now().strftime('%b %d  %H:%M:%S\n'))
#     # #     sleep(0.95)
#     # # else:
#     # #     sleep(0.01)
#     lcd.write_string("Registro de ponto")
#     id, ra = leitorRfid.read()
#     print("ID do aluno: ", id)
#     lcd.clear()

#     if id == 383529815217:
#         hit_point(id)
#         lcd.write_string("Tag RFID válida")
#         time.sleep(5)
#         GPIO.cleanup()
#         loop == False
#     else:
#         lcd.write_string("Tag RFID nao permitida!")
#         time.sleep(5)
#         GPIO.cleanup()
#         loop == False

# if loop == False:
#     loop = True
