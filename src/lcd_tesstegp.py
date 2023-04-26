import time
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from RPLCD import CharLCD

# Configuração do leitor RFID
reader = SimpleMFRC522()

# Configuração do display LCD
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

# Loop principal
while True:
    # Exibe a hora atual no display
    lcd.cursor_pos = (0, 0)
    lcd.write_string(time.strftime("%H:%M:%S"))

    # Verifica se um cartão RFID foi aproximado
    try:
        id, text = reader.read()
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Tag valida ")
    except:
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Tag invalida")

    # Aguarda 1 segundo antes de atualizar o display novamente
    time.sleep(1)
