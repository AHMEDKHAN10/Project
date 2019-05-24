import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests
import random
import urllib.request
import webbrowser
new=2
import string

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
fan = 22
GPIO.setup(fan, GPIO.OUT)
led = 17
GPIO.setup(led, GPIO.OUT)
#GPIO.cleanup()
GPIO_TRIGGER = 23
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def thingspeak_post():#to post data on cloud(webhook)
    val= checkdist()
    URL='https://api.thingspeak.com/update?api_key='
    KEY='V8AUVCWOQVSYMJ8B'
    HEADER='&field1={}&field2={}'.format(val,val)
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    
    
def checkdist():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

pwm = GPIO.PWM(led, 80)



pwm.start(0)

reading = dht11.DHT11(pin=27)

while True:
    result = reading.read()
    if result.is_valid():
        print("temperature : " + str(datetime.datetime.now()))
        print("temp %d C" % result.temperature)
    if result.temperature>60:
        GPIO.Output(fan,True)
    dist = checkdist()
    print ("Measured Distance = %.1f cm" % dist)
    time.sleep(1)
    if checkdist()<200:        
        print("motion detected")
        if 180<checkdist()<200:
            pwm.ChangeDutyCycle(10)
        elif 160<checkdist()<180:
            pwm.ChangeDutyCycle(20)
        elif 140<checkdist()<160:
            pwm.ChangeDutyCycle(30)
        elif 120<checkdist()<140:
            pwm.ChangeDutyCycle(40)
        elif 100<checkdist()<120:
            pwm.ChangeDutyCycle(60)
        elif 80<checkdist()<100:
            pwm.ChangeDutyCycle(70)
        elif 60<checkdist()<80:
            pwm.ChangeDutyCycle(80)
        elif 40<checkdist()<60:
            pwm.ChangeDutyCycle(90)
        elif 10<checkdist()<40:
            pwm.ChangeDutyCycle(100)
        else:
            pwm.ChangeDutyCycle(0)
        URl = "file:///home/pi/DHT11_Python/photon.html"
        webbrowser.open(URl, new=new)
        r = requests.get("https://maker.ifttt.com/trigger/motion_detected/with/key/cmufi-05TgWCycEdZAwKTr/" )
    thingspeak_post()
    time.sleep(2)

      
#except KeyboardInterrupt:
    #print("Measurement stopped by User")
    #time.sleep(1)
    
pwm.stop()
GPIO.cleanup()
