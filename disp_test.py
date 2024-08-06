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

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import threading
from fastapi.middleware.cors import CORSMiddleware


def scroll_message(message, stop_event):
    message = message.ljust(lcd_columns)
    delay = 0.5
    while not stop_event.is_set():
        for i in range(len(message) - lcd_columns + 1):
            lcd.clear()
            lcd.message(message[i:i + lcd_columns])
            time.sleep(delay)

def scroll_message(message, stop_event):
    message = message.ljust(lcd_columns)
    delay = 0.5
    while not stop_event.is_set():
        for i in range(len(message) - lcd_columns + 1):
            if stop_event.is_set():
                break
            lcd.clear()
            lcd.message(message[i:i + lcd_columns])
            time.sleep(delay)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
stop_event = threading.Event()
thread = threading.Thread(target=scroll_message, args=("                 ", stop_event))
thread.start()

@app.get("/message")
async def receive_message(request: Request, message):
    try:
        global thread  # Use global keyword to access the same thread object
        if thread.is_alive():
            stop_event.set()  # Stop the currently running thread
            thread.join()  # Wait for the thread to finish
            stop_event.clear()  # Clear the stop event
        if len(message) > 16:
            message = "  " + message + "  "
            stop_event.clear()
            thread = threading.Thread(target=scroll_message, args=(message, stop_event))
            thread.start()
        else:
            lcd.clear()
            lcd.message(message)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.25", port=8000)
