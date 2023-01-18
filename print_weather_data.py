import time
import Adafruit_CharLCD as LCD
import os
#Raspberry Pi pin configuration:
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

while True:
    try:
        f = open("temps.txt", "r")
        data = f.read()
        f.close()
        os.system("clear; date")
        print("Printing Data: ")
        print(data)
        outside_temperature = data.split("\n")[0].split(" ")[1]
        outside_humidity = data.split("\n")[1].split(" ")[1]
        inside_temperature = data.split("\n")[2].split(" ")[1]
        inside_humidity = data.split("\n")[3].split(" ")[1]
        outside_str = "Out Temp: " + outside_temperature + "\n" + "Out Hum: " + outside_humidity
        lcd.message(outside_str)
        time.sleep(5)
        lcd.clear()
        inside_str = "In Temp: " + inside_temperature + "\n" + "In Hum: " + inside_humidity
        lcd.message(inside_str)
        time.sleep(5)
        lcd.clear()
    except:
        os.system("clear")
        print("interrupted unexpectedly")
        lcd.clear()
        time.sleep(10)
        lcd.message("No Data")
        time.sleep(60)

