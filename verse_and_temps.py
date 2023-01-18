import requests
import json
import time
import Adafruit_CharLCD as LCD
import os

verse = ""
reference = ""
display_text = ""

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
        # Demo scrolling message right/left.
        lcd.clear()
        i = 0
        DISPLAY_INSIDE = True
        weather_data = "No Data"
        inside_str = "No inside data"
        outside_str = "No ouside data"
        while True:
        
            if(i+16 > len(display_text)):
                i = 0
                time.sleep(3)
                lcd.clear()
                #get temps
                f = open("temps.txt", "r")
                data = f.read()
                f.close()
                outside_temperature = data.split("\n")[0].split(" ")[1]
                outside_humidity = data.split("\n")[1].split(" ")[1]
                inside_temperature = data.split("\n")[2].split(" ")[1]
                inside_humidity = data.split("\n")[3].split(" ")[1]
                outside_str = "OT:" + outside_temperature + " OH:" + outside_humidity
                inside_str = "IT:" + inside_temperature + " IH:" + inside_humidity
                
                #get verse of the day
                url = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"
                headers = {"accept": "application/json"}
                response = requests.get(url, headers=headers)
                verse = json.loads(response.text)['verse']['details']['text']
                reference = json.loads(response.text)['verse']['details']['reference']
                display_text = verse + " - " + reference
                
                os.system("clear")
            snippet = display_text[0+i:16+i]

            
            if(i%10 == 0):
                lcd.clear()
                if(DISPLAY_INSIDE):
                    weather_data = inside_str
                else:
                    weather_data = outside_str
                DISPLAY_INSIDE = not DISPLAY_INSIDE
                
            print(weather_data + "\n" + snippet)
            lcd.message(weather_data + "\n" + snippet)
            
            time.sleep(0.5)
            i = i+1


    except:
        os.system("clear")
        print("interrupted unexpectedly")
        lcd.clear()
        time.sleep(10)
        lcd.message("No Data")
        time.sleep(60)


